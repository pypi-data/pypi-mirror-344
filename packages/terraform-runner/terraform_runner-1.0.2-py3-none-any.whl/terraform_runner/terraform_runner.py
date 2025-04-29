import os
import subprocess
import time
import requests

# absolute path where the Terraform binary is copied during build
TERRAFORM_BIN = "/usr/local/bin/terraform"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# ── helpers ─────────────────────────────────────────────────────────────────────
def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram env vars missing, skipping message.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(
            url,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"},
            timeout=10,
        )
    except Exception as e:
        print(f"Telegram send failed: {e}")


# ── terraform wrappers ──────────────────────────────────────────────────────────
def init_terraform(work_dir: str):
    send_telegram_message(f"🔄 Initializing Terraform in `{work_dir}`...")
    subprocess.run([TERRAFORM_BIN, "init"], cwd=work_dir, check=True)
    send_telegram_message(f"✅ Terraform init completed in `{work_dir}`.")


def plan_terraform(work_dir: str):
    send_telegram_message(f"📋 Generating Terraform plan in `{work_dir}`...")
    subprocess.run([TERRAFORM_BIN, "plan"], cwd=work_dir, check=True)
    send_telegram_message(f"✅ Terraform plan generated in `{work_dir}`.")


def apply_terraform_with_retries(
    work_dir: str, max_retries: int = 3, delay_seconds: int = 5
):
    for attempt in range(1, max_retries + 1):
        try:
            send_telegram_message(
                f"🚀 Applying Terraform (Attempt {attempt}/{max_retries})..."
            )
            subprocess.run(
                [TERRAFORM_BIN, "apply", "-auto-approve"],
                cwd=work_dir,
                check=True,
            )
            send_telegram_message(
                f"✅ Terraform apply succeeded on attempt {attempt}."
            )
            return
        except subprocess.CalledProcessError:
            send_telegram_message(
                f"⚠️ Terraform apply failed on attempt {attempt}. "
                f"Retrying in {delay_seconds} s…"
            )
            time.sleep(delay_seconds)

    send_telegram_message(f"❌ Terraform apply failed after {max_retries} attempts.")
    raise Exception("Terraform apply failed after retries.")


def get_terraform_outputs(work_dir: str):
    send_telegram_message("📤 Retrieving Terraform outputs…")
    out = subprocess.run(
        [TERRAFORM_BIN, "output", "-json"],
        cwd=work_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout


# ── public entrypoint ───────────────────────────────────────────────────────────
def deploy_agent(work_dir: str):
    try:
        init_terraform(work_dir)
        plan_terraform(work_dir)
        apply_terraform_with_retries(work_dir)
        outputs = get_terraform_outputs(work_dir)
        send_telegram_message(
            f"✅ Deployment complete!\n\n*Outputs:*\n```{outputs}```"
        )
        return outputs
    except Exception as e:
        send_telegram_message(f"❌ Deployment failed with error: {e}")
        raise
