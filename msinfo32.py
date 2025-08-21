from pathlib import Path
from datetime import datetime
import subprocess
import smtplib
from email.message import EmailMessage

def sysInfo():
    desktop = Path.home() / "Desktop"
    outDir = desktop / "SystemInfo"
    outDir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outFile = outDir / f"system_info_{timestamp}.nfo"

    try:
        subprocess.run(["msinfo32", "/nfo", str(outFile)], check=True)
        print(f"System information exported to: {outFile}")
        return outFile
    except subprocess.CalledProcessError as e:
        print(f"Error exporting system information: {e}")
    except FileNotFoundError:
        print("msinfo32 not found. This script must be run on Windows.")

def sendEmail(recipient, subject, body, attachment_path, sender, password):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)
    
    # Attach the file
    with open(attachment_path, "rb") as f:
        fileData = f.read()
        filename = Path(attachment_path).name
    msg.add_attachment(fileData, maintype="application", subtype="octet-stream", filename=filename)

    # Send the email (Gmail SMTP example)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
    print("Email sent.")

if __name__ == "__main__":
    outFile = sysInfo()
    if outFile:
        recipient = "email@email.com"
        subject = "System Information"
        body = "MSinfo32 from a computer."
        sender = "your email"        
        password = "XXXX XXXX XXXX XXXX" #App Password (from email)
        sendEmail(recipient, subject, body, outFile, sender, password)


