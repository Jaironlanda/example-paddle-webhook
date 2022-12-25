## Paddle Webhook with FastAPI (Example)

This is example payment for sell one-time products only.

More info: https://developer.paddle.com/webhook-reference

## Paddle Public Key

1. Rename `.env-temp` to `.env`
2. Set `PADDLE_PUBLIC_KEY`. You can get this from Paddle dashboard > Developer tools > Public Key

## Install
`pip install -r requirements.txt`

## Run

`uvicorn main:app --reload`
