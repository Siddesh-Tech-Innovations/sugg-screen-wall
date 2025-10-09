# Suggestion Screen Wall - Documentation

This folder contains all documentation for the Suggestion Screen Wall application.

## Documentation Overview

### Setup and Integration
- [INTEGRATION_SETUP.md](./INTEGRATION_SETUP.md) - Step-by-step setup guide for connecting frontend to backend
- [INTEGRATION_COMPLETE.md](./INTEGRATION_COMPLETE.md) - Complete integration summary and recommendations

### Backend Documentation
- [Backend-Documentation.md](./Backend-Documentation.md) - Comprehensive backend API documentation

### Architecture Diagrams
- [Functional Architecture.png](./Functional%20Architecture.png) - High-level functional architecture diagram
- [Tech Architecture.png](./Tech%20Architecture.png) - Technical architecture diagram

## Quick Start

1. Follow the [INTEGRATION_SETUP.md](./INTEGRATION_SETUP.md) for complete setup instructions
2. Review [Backend-Documentation.md](./Backend-Documentation.md) for API details
3. Check [INTEGRATION_COMPLETE.md](./INTEGRATION_COMPLETE.md) for implementation recommendations

## Project Structure

```
sugg-screen-wall/
├── frontend/           # React application with canvas drawing
├── backend/            # FastAPI backend with OCR processing
├── docs/              # All documentation files
└── myscript-sdk/      # Additional SDK components
```

## Technology Stack

### Frontend
- React 19.2.0
- HTML5 Canvas for drawing
- Fetch API for backend communication

### Backend
- FastAPI (Python)
- MongoDB with Motor (async driver)
- OCR processing (Tesseract/Google Vision/OpenAI options)
- Rate limiting and security features

## Getting Help

For setup issues or questions:
1. Check the setup guide in [INTEGRATION_SETUP.md](./INTEGRATION_SETUP.md)
2. Review troubleshooting section in the documentation
3. Verify all dependencies are installed correctly