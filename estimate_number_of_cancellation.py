import re
import math
import time

import requests
from bs4 import BeautifulSoup


from typing import List
IdList = List[str]


def calc_participation_rate(user_id: str, new_user_participation_prob: float = 0.5) -> float:
    """イベント参加予定者の過去のイベントに実際に参加した割合を求め、参加確率とする

    Args:
        user_id (str): ユーザid
        new_user_participation_prob (float, optional): 新規ユーザの場合の確率. Defaults to 0.5.

    Returns:
        float: イベント参加確率
    """
    user_url = f'https://connpass.com/user/{user_id}/'
    r = requests.get(user_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    participating_total_num = int(
        soup.select('.square_tab .num')[0].get_text())

    if participating_total_num == 0:
        return new_user_participation_prob

    page_total_num = math.ceil(participating_total_num / 10.)

    total_register_num = 0
    participate_num = 0

    for page_idx in range(1, page_total_num + 1):
        if page_idx > 1:
            time.sleep(1)
            user_url = f'https://connpass.com/user/{user_id}/?page={page_idx}'
            r = requests.get(user_url)
            soup = BeautifulSoup(r.text, 'html.parser')

        results = soup.select('div.event_area .event_list')
        for result in results:
            result2 = result.select('.event_thumbnail .label_status_event')

            if result2[0].get_text() == '終了':
                participate_status = result.select(
                    '.label_status_tag')[0].get_text()

                if participate_status == '補欠':
                    continue

                total_register_num += 1

                if participate_status == 'キャンセル':
                    continue
                else:
                    participate_num += 1

    participation_rate = participate_num / total_register_num

    print(f"ユーザID: {user_id}, 参加確率: {participation_rate}, 参加回数: {participate_num}, イベント申し込み数: {total_register_num}")

    return participation_rate


def get_participants_id_list(event_url: str) -> IdList:
    """イベント参加予定者のユーザidのリストを取得

    Args:
        event_url (str): イベントページのURL

    Returns:
        IdList: ユーザidのリスト
    """
    participants_url = f'{event_url}/participation'

    r = requests.get(participants_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    participants_id_list = []

    for participation_table_list in soup.select('.participation_table_area'):
        for participating_user in participation_table_list.select('.user'):
            user_url = participating_user.select('.display_name a')[0]['href']
            m = re.match('https://connpass.com/user/(.*)/', user_url)
            participants_id_list.append(m.group(1))

    # 重複するユーザidを除外
    # イベント関係者がイベント申し込み者にいる場合があるため。
    participants_id_list = list(set(participants_id_list))

    return participants_id_list


if __name__ == '__main__':
    import sys
    participants_id_list = get_participants_id_list(sys.argv[1])
    print('イベントに参加予定のユーザIDリスト')
    print(participants_id_list)
    print()

    candidate_num = len(participants_id_list)
    sum_rate = 0
    print(f"全{candidate_num}ユーザー分の参加確率を算出中...")
    for participants_id in participants_id_list:
        rate = calc_participation_rate(participants_id)
        sum_rate += rate
    print()

    print(
        f"見積もったキャンセル人数: {candidate_num - sum_rate}, 現在の参加登録人数: {candidate_num}, 現在の参加人数の期待値:{sum_rate}")
