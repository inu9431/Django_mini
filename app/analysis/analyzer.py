import io
from datetime import date

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")

from django.core.files.base import ContentFile
from app.budgets.models import Transaction

class Analyzer:
    def __init__(self, user, period_start: date, period_end: date):
        self.user = user
        self.period_start = period_start
        self.period_end = period_end

    def get_dataframe(self):
        transactions = Transaction.objects.filter(
            account__user=self.user,
            date__range=(self.period_start, self.period_end),
        ).values("date", "type", "amount")
        return pd.DataFrame(list(transactions))

    def generate_image(self):
        df = self.get_dataframe()

        if df.empty:
            return None

        df["amount"] = df["amount"].astype(float)
        summary = df.groupby("type")["amount"].sum()

        fig, ax = plt.subplots()
        summary.plot(kind="bar", ax=ax, color=["green", "red"])
        ax.set_title(f"{self.period_start} ~ {self.period_end}")
        ax.set_ylabel("금액 (원)")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        filename = f"{self.user.id}_{self.period_start}_{self.period_end}.png"
        return ContentFile(buf.read(), name=filename)

    def analyze(self, about, period_type):
        from app.analysis.models import Analysis

        image = self.generate_image()

        analysis = Analysis(
            user=self.user,
            about=about,
            type=period_type,
            period_start=self.period_start,
            period_end=self.period_end,
        )

        if image:
            analysis.result_image.save(image.name, image, save=False)

        analysis.save()
        return analysis


