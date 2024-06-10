sudo apt update
sudo apt install curl

curl -fsSL https://ollama.com/install.sh | sh
pip install ollama --break-system-packages

ollama --version