import logging

from spaceone.core import cache
from spaceone.core.manager import BaseManager

from spaceone.monitoring.error.project_alert_config import *
from spaceone.monitoring.model.project_alert_config_model import ProjectAlertConfig

_LOGGER = logging.getLogger(__name__)


class ProjectAlertConfigManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_alert_config_model: ProjectAlertConfig = self.locator.get_model(
            "ProjectAlertConfig"
        )

    def create_project_alert_config(self, params: dict) -> ProjectAlertConfig:
        def _rollback(vo: ProjectAlertConfig):
            _LOGGER.info(
                f"[create_project_alert_config._rollback] "
                f"Delete project alert config : {vo.project_id}"
            )
            vo.delete()

        project_alert_config_vo: ProjectAlertConfig = (
            self.project_alert_config_model.create(params)
        )
        self.transaction.add_rollback(_rollback, project_alert_config_vo)

        return project_alert_config_vo

    def update_project_alert_config(self, params):
        project_alert_config_vo: ProjectAlertConfig = self.get_project_alert_config(
            params["project_id"], params["workspace_id"], params["domain_id"]
        )
        return self.update_project_alert_config_by_vo(params, project_alert_config_vo)

    def update_project_alert_config_by_vo(
        self, params: dict, project_alert_config_vo: ProjectAlertConfig
    ) -> ProjectAlertConfig:
        def _rollback(old_data: dict):
            _LOGGER.info(
                f"[update_project_alert_config_by_vo._rollback] Revert Data : "
                f'{old_data["project_id"]}'
            )
            project_alert_config_vo.update(old_data)

        self.transaction.add_rollback(_rollback, project_alert_config_vo.to_dict())

        updated_vo: ProjectAlertConfig = project_alert_config_vo.update(params)

        cache.delete(
            f"monitoring:alert:project-options:{updated_vo.domain_id}:{updated_vo.project_id}"
        )
        cache.delete(
            f"monitoring:escalation-policy-info:{updated_vo.domain_id}:{updated_vo.project_id}"
        )
        cache.delete(
            f"monitoring:auto-recovery:{updated_vo.domain_id}:{updated_vo.project_id}"
        )

        return updated_vo

    def delete_project_alert_config(
        self, project_id: str, domain_id: str, workspace_id: str
    ):
        project_alert_config_vo: ProjectAlertConfig = self.get_project_alert_config(
            project_id, workspace_id, domain_id
        )

        cache.delete(f"monitoring:alert:project-options:{domain_id}:{project_id}")
        cache.delete(f"monitoring:escalation-policy-info:{domain_id}:{project_id}")
        cache.delete(f"monitoring:auto-recovery:{domain_id}:{project_id}")

        project_alert_config_vo.delete()

    def get_project_alert_config(
        self, project_id: str, workspace_id: str, domain_id: str
    ) -> ProjectAlertConfig:
        try:
            return self.project_alert_config_model.get(
                project_id=project_id, workspace_id=workspace_id, domain_id=domain_id
            )
        except ERROR_NOT_FOUND as e:
            raise ERROR_ALERT_FEATURE_IS_NOT_ACTIVATED(
                project_id=project_id, workspace_id=workspace_id
            )
        except Exception as e:
            raise e

    def list_project_alert_configs(self, query: dict) -> dict:
        return self.project_alert_config_model.query(**query)

    def stat_project_alert_configs(self, query: dict) -> dict:
        return self.project_alert_config_model.stat(**query)
