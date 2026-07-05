import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime


class PDFReport:

    def generate(
        self,
        data,
        prediction,
        confidence,
        recommendation,
    ):
        print(">>> generate() function called")

        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"reports/vehicle_health_report_{timestamp}.pdf"

        os.makedirs("reports", exist_ok=True)

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>Vehicle Health Report</b>",
                styles["Title"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"Generated: {datetime.now()}",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 15))

        fields = [

            ("Prediction", prediction),

            ("Confidence", f"{confidence:.2f}%"),

            ("Motor Health", f"{data.get('Motor Health',100):.1f}%"),

            ("Battery Health", f"{data.get('Battery Health',100):.1f}%"),

            ("Brake Health", f"{data.get('Brake Health',100):.1f}%"),

            ("Tyre Health", f"{data.get('Tyre Health',100):.1f}%"),

            ("Motor Temperature", f"{data['Motor Temp']:.1f} °C"),

            ("Battery Voltage", f"{data['Battery Voltage']:.1f} V"),

            ("Speed", f"{data['Speed']:.1f} km/h"),

            ("RPM", f"{int(data['RPM'])}"),

            ("Recommendation", recommendation["action"]),

            ("Inspection", recommendation["inspection"]),

            ("Priority", recommendation["priority"]),
        ]

        for key, value in fields:

            story.append(
                Paragraph(
                    f"<b>{key}</b>: {value}",
                    styles["BodyText"],
                )
            )

            story.append(Spacer(1, 8))

        doc.build(story)

        print("PDF saved to:", os.path.abspath(filename))

        return filename