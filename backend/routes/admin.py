from fastapi import APIRouter, Depends, Request, HTTPException, Query
from database import db
from models import BulkViewUpdate, SubmissionInDB, AdminUser
from typing import List, Dict, Any
from datetime import datetime
from bson import ObjectId
from utils.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/submissions", summary="Get all submissions with pagination and filtering")
async def get_submissions(page: int = 1, limit: int = 20, viewed: bool = None):
    query = {}
    if viewed is not None:
        query["viewed"] = viewed

    submissions_cursor = db.submissions.find(query).sort("created_at", -1).skip((page - 1) * limit).limit(limit)
    submissions = [SubmissionInDB(**doc) async for doc in submissions_cursor]

    total = await db.submissions.count_documents(query)

    return {
        "success": True,
        "data": {
            "submissions": submissions,
            "pagination": {
                "currentPage": page,
                "totalItems": total,
                "totalPages": (total + limit - 1) // limit,
                "itemsPerPage": limit
            }
        }
    }

@router.patch("/submissions/bulk-view", summary="Mark multiple submissions as viewed")
async def mark_bulk_viewed(payload: BulkViewUpdate):
    object_ids = [ObjectId(i) for i in payload.submission_ids]
    result = await db.submissions.update_many(
        {"_id": {"$in": object_ids}},
        {"$set": {"viewed": True, "updated_at": datetime.utcnow()}}
    )
    return {
        "success": True,
        "message": f"{result.modified_count} submissions marked as viewed",
        "data": {"updated_count": result.modified_count}
    }

@router.get("/submissions/{id}", response_model=SubmissionInDB, summary="Get a single submission by ID")
async def get_submission(id: str):
    submission = await db.submissions.find_one({"_id": ObjectId(id)})
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission

@router.patch("/submissions/{id}/view", summary="Mark a single submission as viewed")
async def mark_viewed(id: str):
    updated_submission = await db.submissions.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"viewed": True, "updated_at": datetime.utcnow()}},
        return_document=True
    )

    if not updated_submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    return {
        "success": True,
        "message": "Submission marked as viewed",
        "data": SubmissionInDB(**updated_submission)
    }

@router.delete("/submissions/{id}", summary="Delete a submission")
async def delete_submission(id: str):
    result = await db.submissions.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"success": True, "message": "Submission deleted successfully"}

@router.get("/dashboard/stats", summary="Get dashboard statistics")
async def get_dashboard_stats():
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    seven_days_ago = today - datetime.timedelta(days=6)

    pipeline = [
        {
            "$facet": {
                "general_stats": [
                    {
                        "$group": {
                            "_id": None,
                            "total_submissions": {"$sum": 1},
                            "unviewed_count": {
                                "$sum": {"$cond": [{"$eq": ["$viewed", False]}, 1, 0]}
                            },
                            "today_count": {
                                "$sum": {"$cond": [{"$gte": ["$created_at", today]}, 1, 0]}
                            },
                            "week_count": {
                                "$sum": {"$cond": [{"$gte": ["$created_at", seven_days_ago]}, 1, 0]}
                            }
                        }
                    }
                ],
                "category_breakdown": [
                    {"$group": {"_id": "$category", "count": {"$sum": 1}}}
                ],
                "sentiment_breakdown": [
                    {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
                ],
                "recent_activity": [
                    {
                        "$match": {
                            "created_at": {"$gte": seven_days_ago}
                        }
                    },
                    {
                        "$group": {
                            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                            "count": {"$sum": 1}
                        }
                    },
                    {"$sort": {"_id": 1}}
                ]
            }
        }
    ]

    result = await db.submissions.aggregate(pipeline).to_list(1)
    if not result:
        # Handle case with no submissions
        return {"success": True, "data": {
            "total_submissions": 0, "unviewed_count": 0, "today_count": 0, "week_count": 0,
            "category_breakdown": {}, "sentiment_breakdown": {}, "recent_activity": []
        }}

    stats = result[0]
    general_stats = stats["general_stats"][0] if stats["general_stats"] else {}
    
    # Format the results to match the desired output structure
    category_breakdown = {item["_id"]: item["count"] for item in stats.get("category_breakdown", []) if item["_id"]}
    sentiment_breakdown = {item["_id"]: item["count"] for item in stats.get("sentiment_breakdown", []) if item["_id"]}
    recent_activity = [{"date": item["_id"], "count": item["count"]} for item in stats.get("recent_activity", [])]

    return {
        "success": True,
        "data": {
            "total_submissions": general_stats.get("total_submissions", 0),
            "unviewed_count": general_stats.get("unviewed_count", 0),
            "today_count": general_stats.get("today_count", 0),
            "week_count": general_stats.get("week_count", 0),
            "category_breakdown": category_breakdown,
            "sentiment_breakdown": sentiment_breakdown,
            "recent_activity": recent_activity
        }
    }
