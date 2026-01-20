from __future__ import annotations

from django.db import models


class AgentTelemetryEvent(models.Model):
    ts_unix = models.FloatField(db_index=True)
    trace_id = models.CharField(max_length=64, db_index=True)

    agent_name = models.CharField(max_length=64, db_index=True)
    agent_version = models.CharField(max_length=32)
    model_name = models.CharField(max_length=128, db_index=True)

    latency_ms = models.IntegerField()

    outcome = models.CharField(max_length=32, db_index=True)
    reason_code = models.CharField(max_length=64, db_index=True)

    prompt_tokens = models.IntegerField(null=True, blank=True)
    completion_tokens = models.IntegerField(null=True, blank=True)
    total_tokens = models.IntegerField(null=True, blank=True)
    estimated_cost_usd = models.FloatField(null=True, blank=True)

    meta = models.JSONField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["agent_name", "ts_unix"]),
            models.Index(fields=["outcome", "ts_unix"]),
        ]
        ordering = ["-ts_unix"]
