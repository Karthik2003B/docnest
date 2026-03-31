from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


def send_email(to_email, subject, otp):
    # 🔥 HTML VERSION (PREMIUM)
    html_content = f"""
    <div style="font-family: Arial, sans-serif; background:#f4f6f8; padding:20px;">
        <div style="max-width:500px; margin:auto; background:white; padding:25px; border-radius:12px;">
            
            <h2 style="color:#0f172a;">DocNest</h2>

            <p style="color:#374151;">Hi,</p>

            <p style="color:#374151;">
                Use the verification code below to complete your sign up:
            </p>

            <div style="text-align:center; margin:25px 0;">
                <span style="
                    font-size:32px;
                    letter-spacing:6px;
                    font-weight:bold;
                    color:#4ea2ad;
                ">
                    {otp}
                </span>
            </div>

            <p style="color:#6b7280; font-size:13px;">
                This code will expire in 5 minutes.
            </p>

            <p style="color:#6b7280; font-size:13px;">
                If you didn’t request this, you can safely ignore this email.
            </p>

            <hr>

            <p style="font-size:12px; color:#9ca3af;">
                You received this email because you signed up for DocNest.
            </p>
        </div>
    </div>
    """

    # 🔥 PLAIN TEXT VERSION (IMPORTANT FOR SPAM FILTERS)
    plain_text = f"""
    DocNest Verification Code

    Your verification code is: {otp}

    This code will expire in 5 minutes.

    If you did not request this, please ignore this email.

    DocNest
    """

    # 🔥 SEND EMAIL
    message = Mail(
        from_email="DocNest <alerts@docnest.me>",   # ✅ keep verified sender
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
        plain_text_content=plain_text
    )

    try:
        sg = SendGridAPIClient(os.getenv("secret_key"))
        sg.send(message)
    except Exception as e:
        print("Email error:", e)