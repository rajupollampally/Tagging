from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Intelligent Deployment Governance Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    REDIS_URL: str
    REDIS_TTL: int = 3600

    KAFKA_BROKERS: str
    KAFKA_TOPIC_DEPLOYMENTS: str
    KAFKA_TOPIC_APPROVALS: str
    KAFKA_TOPIC_BUDGETS: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    SLACK_WEBHOOK_URL: str = ""
    SLACK_BOT_TOKEN: str = ""

    TEAMS_WEBHOOK_URL: str = ""

    JIRA_URL: str = ""
    JIRA_USERNAME: str = ""
    JIRA_API_TOKEN: str = ""

    SERVICENOW_URL: str = ""
    SERVICENOW_USERNAME: str = ""
    SERVICENOW_PASSWORD: str = ""

    JENKINS_URL: str = ""
    JENKINS_USERNAME: str = ""
    JENKINS_API_TOKEN: str = ""

    GITHUB_TOKEN: str = ""
    GITHUB_WEBHOOK_SECRET: str = ""

    AZURE_DEVOPS_URL: str = ""
    AZURE_DEVOPS_PAT: str = ""

    CORS_ORIGINS: str = "[\"*\"]"

    ENABLE_TRACING: bool = True
    JAEGER_HOST: str = ""
    JAEGER_PORT: int = 6831
    ENABLE_METRICS: bool = True

    BUDGET_ALERT_THRESHOLD: float = 1000.0
    BUDGET_CRITICAL_THRESHOLD: float = 5000.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
