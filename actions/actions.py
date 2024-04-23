# actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pathlib import Path
import yaml

# 분야별 정책 출력
class ActionShowPolicies(Action):
    def name(self) -> Text:
        return "action_show_policies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        region = tracker.get_slot('region')
        # 지역에 따라 파일 경로 설정
        if region == '대전':
            file_path = Path(__file__).parent.parent / "data/Daejeon_policies_data.yml"
        elif region == '중앙부처':
            file_path = Path(__file__).parent.parent / "data/All_policies_data.yml"
        else:
            dispatcher.utter_message(text="지원하지 않는 지역입니다.")
            return []

        # 파일에서 데이터 로드
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        policy_field = tracker.get_slot('policies')
        # 선택한 정책 분야에 해당하는 정책 목록 추출
        if policy_field in data['policies']:
            policies = data['policies'][policy_field]
            policy_names = list(policies.keys())
            response = f"{region}의 {policy_field} 정책으로는 " + ", ".join(policy_names) + "가 있습니다."
        else:
            response = "선택하신 정책 분야에 해당하는 정보를 찾을 수 없습니다."

        dispatcher.utter_message(text=response)

        return []


# 정책 정보 출력
class ActionShowPolicySummary(Action):
    def name(self) -> Text:
        return "action_show_policy_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        region = tracker.get_slot('region')  # '대전' 혹은 '중앙부처'
        policy_field = tracker.get_slot('policies')  # 사용자가 선택한 정책 분야
        policy_name = tracker.get_slot('policy')  # 예: '청년내일희망카드'
        info_type = tracker.get_slot('info')  # 예: '요약'

        # 선택된 지역에 따라 파일 경로 설정
        if region == '대전':
            file_path = "data/Daejeon_policies_data.yml"
        elif region == '중앙부처':
            file_path = "data/All_policies_data.yml"
        else:
            dispatcher.utter_message(text="지원하지 않는 지역입니다.")
            return []

        with open(file_path, 'r', encoding="utf-8") as file:
            policies_data = yaml.safe_load(file)

        # 선택된 정책 분야에 따라 정보 검색
        policy_info = policies_data['policies'].get(policy_field, {}).get(policy_name, {}).get(info_type, [])

        for item in policy_info:
            if isinstance(item, dict):
                for key, value in item.items():
                    dispatcher.utter_message(text=f"{key}: {value}")
            else:
                dispatcher.utter_message(text=item)

        return []