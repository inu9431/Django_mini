from rest_framework import serializers
from app.analysis.models import Analysis

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = [
            'id',
            'summary',
            'period_type',
            'period_start',
            'period_end',
            'description',
            'result_image',
            'created_at'
        ]