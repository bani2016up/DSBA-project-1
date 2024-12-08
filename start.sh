

cd app/frontend
echo "Stage 1: Installing dependency for frontend."
poetry lock
poetry install
cd ../
cd backend
echo "Stage 2: Installing dependency for backend."
poetry lock
poetry install
cd ../../
echo ls
echo "Stage 3: Starting docker compose web app."
docker compose up -d --no-deps --build
