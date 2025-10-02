# SpaceD Mission Terminal - Local Docker Setup

Simple Docker setup for testing the hackathon mission terminal locally.

## Quick Start

**Run the SpaceD Mission Terminal exactly like the local version:**

```bash
# Build and run interactively
docker-compose run --rm spaced-terminal
```

This will:
- ✅ Start the mission terminal with full interactive input
- ✅ Give you access to all 9 logs and mission briefings  
- ✅ Work exactly like running the Python script locally
- ✅ **Navigation**: Use arrow keys (↑/↓) or w/s to navigate
- ✅ **Smart Navigation**: 
  - **M** = Main Menu (from anywhere)
  - **L** = Logs Menu (from anywhere) 
  - **R** = Return to specific log (from mission briefing)
  - **Q** = Quit application (from main menu)
- ✅ **Clean screens**: No scrollback interference - each screen is properly cleared

**Alternative commands:**

```bash
# Build first, then run
docker-compose build
docker-compose run --rm spaced-terminal

# Direct Docker commands
docker build -t spaced-mission-terminal .
docker run -it --rm spaced-mission-terminal
```

## What's Included

- **Python 3.11** runtime
- **Rich** for beautiful terminal interfaces
- **Readchar** for keyboard input
- **NumPy** and **ModernGL** for physics simulation
- **Interactive terminal** support with TTY

## For Hackathon Deployment

For Azure deployment, you can:
1. Push this image to Azure Container Registry
2. Deploy to Azure Container Instances or App Service
3. Use the Azure Portal for easy one-click deployment

The container is ready to run in any cloud environment!