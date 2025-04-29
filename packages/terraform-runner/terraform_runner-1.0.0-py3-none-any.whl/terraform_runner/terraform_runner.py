import os
import subprocess
import time
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    """
    Send a Telegram message using the Telegram Bot API.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram env vars missing, skipping message.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        print(f"Telegram send failed: {e}")

def init_terraform(work_dir: str):
    """
    Initialize the Terraform working directory.
    """
    send_telegram_message(f"🔄 Initializing Terraform in `{work_dir}`...")
    subprocess.run(["terraform", "init"], cwd=work_dir, check=True)
    send_telegram_message(f"✅ Terraform init completed in `{work_dir}`.")

def plan_terraform(work_dir: str):
    """
    Create a Terraform plan.
    """
    send_telegram_message(f"📋 Generating Terraform plan in `{work_dir}`...")
    subprocess.run(["terraform", "plan"], cwd=work_dir, check=True)
    send_telegram_message(f"✅ Terraform plan generated in `{work_dir}`.")

def apply_terraform_with_retries(work_dir: str, max_retries: int = 3, delay_seconds: int = 5):
    """
    Apply Terraform plan with retries.
    """
    for attempt in range(1, max_retries + 1):
        try:
            send_telegram_message(f"🚀 Applying Terraform (Attempt {attempt}/{max_retries})...")
            subprocess.run(["terraform", "apply", "-auto-approve"], cwd=work_dir, check=True)
            send_telegram_message(f"✅ Terraform apply succeeded on attempt {attempt}.")
            return
        except subprocess.CalledProcessError as e:
            send_telegram_message(f"⚠️ Terraform apply failed on attempt {attempt}. Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)
    # If we get here, all retries failed
    send_telegram_message(f"❌ Terraform apply failed after {max_retries} attempts.")
    raise Exception("Terraform apply failed after retries.")

def get_terraform_outputs(work_dir: str):
    """
    Retrieve outputs from the Terraform deployment.
    """
    send_telegram_message(f"📤 Retrieving Terraform outputs...")
    output = subprocess.run(["terraform", "output", "-json"], cwd=work_dir, capture_output=True, text=True, check=True)
    return output.stdout

def deploy_agent(work_dir: str):
    """
    Main function to deploy an agent using Terraform.
    """
    try:
        init_terraform(work_dir)
        plan_terraform(work_dir)
        apply_terraform_with_retries(work_dir)
        outputs = get_terraform_outputs(work_dir)
        send_telegram_message(f"✅ Deployment complete!\n\n*Outputs:*\n```{outputs}```")
        return outputs
    except Exception as e:
        send_telegram_message(f"❌ Deployment failed with error: {str(e)}")
        raise
