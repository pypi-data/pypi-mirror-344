import functools
import logging
from typing import List

from spaceone.core import utils
from spaceone.core.connector.space_connector import SpaceConnector
from spaceone.core.manager import BaseManager

from spaceone.monitoring.model.event_rule_model import EventRule, EventRuleCondition

_LOGGER = logging.getLogger(__name__)


class EventRuleManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_rule_model: EventRule = self.locator.get_model("EventRule")
        self._service_account_info = {}

    def create_event_rule(self, params: dict) -> EventRule:
        def _rollback(vo: EventRule):
            _LOGGER.info(
                f"[create_event_rule._rollback] "
                f"Delete event rule : {vo.name} "
                f"({vo.event_rule_id})"
            )
            vo.delete()

        event_rule_vo: EventRule = self.event_rule_model.create(params)
        self.transaction.add_rollback(_rollback, event_rule_vo)

        return event_rule_vo

    def update_event_rule(self, params):
        event_rule_vo: EventRule = self.get_event_rule(
            params["event_rule_id"], params["domain_id"], params["workspace_id"]
        )
        return self.update_event_rule_by_vo(params, event_rule_vo)

    def update_event_rule_by_vo(self, params: dict, event_rule_vo: EventRule):
        def _rollback(old_data: dict):
            _LOGGER.info(
                f"[update_event_rule_by_vo._rollback] Revert Data : "
                f'{old_data["event_rule_id"]}'
            )
            event_rule_vo.update(old_data)

        self.transaction.add_rollback(_rollback, event_rule_vo.to_dict())

        return event_rule_vo.update(params)

    @staticmethod
    def delete_event_rule_by_vo(event_rule_vo):
        event_rule_vo.delete()

    def get_event_rule(
        self,
        event_rule_id: str,
        domain_id: str,
        workspace_id: str,
        user_projects: list = None,
    ):
        conditions = {
            "event_rule_id": event_rule_id,
            "domain_id": domain_id,
            "workspace_id": workspace_id,
        }

        if user_projects:
            conditions["project_id"] = user_projects

        return self.event_rule_model.get(**conditions)

    def list_event_rules(self, query: dict) -> dict:
        return self.event_rule_model.query(**query)

    def filter_event_rules(self, **conditions):
        return self.event_rule_model.filter(**conditions)

    def stat_event_rules(self, query: dict) -> dict:
        return self.event_rule_model.stat(**query)

    def change_event_data(self, event_data, project_id, domain_id, workspace_id):
        event_rule_vos: List[EventRule] = self._get_project_event_rules(
            project_id, domain_id, workspace_id
        )

        for event_rule_vo in event_rule_vos:
            is_match = self._change_event_data_by_event_rule(event_data, event_rule_vo)

            if is_match:
                event_data = self._change_event_data_with_actions(
                    event_data, event_rule_vo.actions, domain_id, workspace_id
                )

            if is_match and event_rule_vo.options.stop_processing:
                break

        return event_data

    def _change_event_data_with_actions(
        self, event_data, actions, domain_id, workspace_id
    ):
        for action, value in actions.items():
            if action == "change_project":
                event_data["project_id"] = value
                if "assignee" in event_data:
                    del event_data["assignee"]
                if "escalation_policy_id" in event_data:
                    del event_data["escalation_policy_id"]

                _LOGGER.debug(
                    f"[_change_event_data_with_actions] change_project: {value}"
                )
                event_data = self.change_event_data(
                    event_data, value, domain_id, workspace_id
                )
            else:
                if action == "change_assignee":
                    event_data["assignee"] = value

                if action == "change_urgency":
                    event_data["urgency"] = value

                if action == "change_escalation_policy":
                    event_data["escalation_policy_id"] = value

                if action == "add_additional_info":
                    event_data["additional_info"] = event_data.get(
                        "additional_info", {}
                    )
                    event_data["additional_info"].update(value)

                if action == "no_notification":
                    event_data["no_notification"] = value

        return event_data

    def _change_event_data_by_event_rule(self, event_data, event_rule_vo: EventRule):
        conditions_policy = event_rule_vo.conditions_policy

        if conditions_policy == "ALWAYS":
            return True
        else:
            results = list(
                map(
                    functools.partial(self._check_condition, event_data),
                    event_rule_vo.conditions,
                )
            )

            if conditions_policy == "ALL":
                return all(results)
            else:
                return any(results)

    @staticmethod
    def _check_condition(event_data, condition: EventRuleCondition):
        event_value = utils.get_dict_value(event_data, condition.key)
        condition_value = condition.value
        operator = condition.operator

        if event_value is None:
            return False

        if operator == "eq":
            if event_value == condition_value:
                return True
            else:
                return False
        elif operator == "contain":
            if event_value.lower().find(condition_value.lower()) >= 0:
                return True
            else:
                return False
        elif operator == "not":
            if event_value != condition_value:
                return True
            else:
                return False
        elif operator == "not_contain":
            if event_value.lower().find(condition_value.lower()) < 0:
                return True
            else:
                return False

        return False

    def _get_project_event_rules(self, project_id, domain_id, workspace_id):
        query = {
            "filter": [
                {"k": "project_id", "v": project_id, "o": "eq"},
                {"k": "domain_id", "v": domain_id, "o": "eq"},
                {"k": "workspace_id", "v": workspace_id, "o": "eq"},
            ],
            "sort": [{"key": "order"}],
        }

        event_rule_vos, total_count = self.list_event_rules(query)
        return event_rule_vos

    def _get_service_account(self, target_key, target_value, domain_id):
        if f"{domain_id}:{target_key}:{target_value}" in self._service_account_info:
            return self._service_account_info[
                f"{domain_id}:{target_key}:{target_value}"
            ]

        query = {
            "filter": [{"k": target_key, "v": target_value, "o": "eq"}],
            "only": ["service_account_id", "project_info"],
        }

        identity_connector: SpaceConnector = self.locator.get_connector(
            "SpaceConnector", service="identity"
        )
        response = identity_connector.dispatch(
            "ServiceAccount.list", {"query": query, "domain_id": domain_id}
        )

        results = response.get("results", [])
        total_count = response.get("total_count", 0)

        service_account_info = None
        if total_count > 0:
            service_account_info = results[0]

        self._service_account_info[f"{domain_id}:{target_key}:{target_value}"] = (
            service_account_info
        )
        return service_account_info
