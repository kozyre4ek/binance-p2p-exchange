docker run --rm -d \
    --env-file .env_docker \
    -p 80:80 \
    binance-p2p-exchange-api:1.0.0