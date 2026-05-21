<!-- Brief architecture note for the food waste carbon estimation system. -->

# System Architecture

`frontend` is a React + Vite client responsible for image upload, total waste weight input, and result presentation.

`backend` is a FastAPI service that receives the image, runs YOLOv11 inference, estimates each food item's weight from object area and `density_factor`, calculates carbon emissions from `carbon_factor`, and stores the analysis into PostgreSQL.

`database` contains the PostgreSQL bootstrap SQL for the system tables and starter food factor data.

`docker-compose.yml` orchestrates `frontend`, `backend`, `postgres`, and optional `pgadmin`.
