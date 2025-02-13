# -*- coding: utf-8 -*-
# python
import os, traceback
# third-party
from flask import Blueprint
# sjva 공용
from framework.logger import get_logger
from framework import app, path_data
from framework.util import Util
from plugin import get_model_setting, Logic, default_route, PluginUtil
# 패키지
#########################################################
class P(object):
    package_name = __name__.split('.')[0]
    logger = get_logger(package_name)
    blueprint = Blueprint(package_name, package_name, url_prefix='/%s' %  package_name, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    menu = {
        'main' : [package_name, u'비디오 다운로드'],
        'sub' : [
            ['ani365', u'ani365'], ['aniplus', u'ANIPLUS'], ['twitch', u'Twitch live'], ['log', u'로그']
        ], 
        'category' : 'vod',
        'sub2' : {
            'ani365' : [
                ['setting', u'설정'], ['request', u'요청'], ['queue', u'큐'], ['list', u'목록']
            ],
            'aniplus' : [
                ['setting', u'설정'], ['request', u'요청'], ['queue', u'큐'], ['list', u'목록']
            ],
            'twitch' : [
                ['setting', u'설정'], ['status', u'상태'], ['list', u'목록']
            ]
        }
    }  
    plugin_info = {
        'version' : '0.2.1.0',
        'name' : 'downloader_video',
        'category_name' : 'vod',
        'icon' : '',
        'developer' : 'soju6jan',
        'description' : u'비디오 다운로드',
        'home' : 'https://github.com/soju6jan/downloader_video',
        'more' : '',
    }
    ModelSetting = get_model_setting(package_name, logger)
    logic = None
    module_list = None
    home_module = 'ani365'


def initialize():
    try:
        app.config['SQLALCHEMY_BINDS'][P.package_name] = 'sqlite:///%s' % (os.path.join(path_data, 'db', '{package_name}.db'.format(package_name=P.package_name)))
        PluginUtil.make_info_json(P.plugin_info, __file__)
        from .logic_ani365 import LogicAni365
        from .logic_aniplus import LogicAniplus
        from .logic_twitch import LogicTwitch
        P.module_list = [LogicAni365(P), LogicAniplus(P), LogicTwitch(P)]
        P.logic = Logic(P)
        default_route(P)
    except Exception as e: 
        P.logger.error('Exception:%s', e)
        P.logger.error(traceback.format_exc())

initialize()
