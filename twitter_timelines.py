import argparse

import time
from twitter_api import TwitterFeeds
from db_util import MongoDBActor
from datetime import datetime


class TwitterTimeline:
    def __init__(self, screen_name):
        self.screen_name = screen_name

    def process(self):
        _is_fetch_success = self.fetch_user_if_not_present()
        if not _is_fetch_success:
            return
        _numeric_id = self.get_user_id_from_user_detail()
        if not _numeric_id:  # chances are account is suspended
            return

        # fetch timeline from last timestamp of fetched
        may_be_last_time_line = self.get_time_lines_last_created_date()

        if may_be_last_time_line is not None:
            _timelines = TwitterFeeds().get_user_tweets(numeric_user_id=_numeric_id,
                                                        _additional_query_param={
                                                            'start_time': may_be_last_time_line
                                                        })
        else:
            _timelines = TwitterFeeds().get_user_tweets(numeric_user_id=_numeric_id)
        for _tl in _timelines:
            _tl['screen_name'] = self.screen_name
            _tl['id'] = _numeric_id
            _insert = MongoDBActor("twitter_timeline").insert_data(_tl)
        time.sleep(1)

    def fetch_user_if_not_present(self, do_wait=None, wait=3):
        retry = 0
        while retry < 5:
            is_account_present = self.is_user_detail_existent()
            if is_account_present:
                return True
            if not is_account_present:
                try:
                    _user_info = TwitterFeeds(self.screen_name).fetch_user_detail_by_screen_name()
                    if do_wait:
                        time.sleep(wait)
                    if _user_info is not None:
                        MongoDBActor("twitter_user").find_and_modify(
                            key={'screen_name': self.screen_name},
                            data={
                                'screen_name': self.screen_name,
                                'detail': _user_info
                            })
                        return True
                except Exception as ex:
                    print("Exception occurred {}".format(ex))
                    time.sleep(10)

            retry += retry + 1
        return False

    def is_user_detail_existent(self):
        _data = MongoDBActor("twitter_user").find(key={'screen_name': self.screen_name})
        for _d in _data:
            if 'screen_name' in _d:
                return True
        return False

    def get_time_lines_last_created_date(self):
        tl = MongoDBActor("twitter_timeline").distinct(key="created_at", filter={'screen_name': self.screen_name})
        if None in tl:
            tl.remove(None)

        if len(tl) == 0:
            return None

        tl.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z"), reverse=True)
        print("Found timelines existed created:{}".format(list(tl)))
        return tl[0]

    def get_user_id_from_user_detail(self):
        try:
            for val in MongoDBActor("twitter_user").find(key={'screen_name': self.screen_name}):
                if 'detail' in val:
                    _detail = val['detail']
                    if _detail:
                        if 'data' in _detail:
                            _data = _detail['data']
                            if len(_data) > 0:
                                _user_nested_info = _data[0]
                                if 'id' in _user_nested_info:
                                    _id = _user_nested_info['id']
                                    return _id
        except Exception as ex:
            print("Exception occurred! {}".format(ex))

        return None


if __name__ == "__main__":
    _arg_parser = argparse.ArgumentParser(description="Process timeline data collect")
    _arg_parser.add_argument("-s", "--screen_name",
                             action="store",
                             required=True,
                             help="Each twitter timeline data to collect")

    _arg_value = _arg_parser.parse_args()
    time_line = TwitterTimeline(_arg_value.screenPname)
    time_line.process()
