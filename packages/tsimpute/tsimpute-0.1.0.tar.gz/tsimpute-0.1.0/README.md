# 📉 Time Series Imputation 📈

Time Series Imputation Capstone Project (FPT University Da Nang).

## 🎓 Authors

- Phan Thị Thu Hồng (Supervisor)
- Đinh Thiều Quang
- Đào Ngọc Huy
- Đoàn Quang Minh - quangminh57dng@gmail.com
- Lê Thị Minh Thư

## 🚀 Run this code

### Prerequisite

- Install `Python>=3.11`.

- Install project dependencies

```sh
# Install python package manager
pip install poetry
# Install dependencies
poetry install
```

- Make sure you have your own data (`.csv` file) in `data` folder.

### Run with manual configs

- Open `notebooks/default.ipynb`.

## 🐳 Docker

- Build image

```sh
docker build -t mingdoan/tsimpute-runner -f ./docker/runner.Dockerfile .
```

- Export experiment config

```sh
python docker/exp.py -f settings/your_config.yml
```

- Start MLFlow & MinIO

```sh
docker compose up -d
```
