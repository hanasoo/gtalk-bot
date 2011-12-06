# -*- coding:utf-8 -*-

import re, random

# Action keies

TRIGGERS = [
	re.compile('(?P<s>[\d]{1,2})時.*?(?P<e>[\d]{1,2})時(?:まで|、)*(?:(?P<r>Grande|Tall|Short)(?:で|,)*)*(?P<t>.*)'),
	re.compile('(?P<s>[\d]{1,2})-(?P<e>[\d]{1,2}) (?P<r>Grande|Tall|Short) (?P<t>.*)'),
	re.compile('(Grande|Tall|Short)'),
	re.compile('時'),
	re.compile('(おはよう|こんにちわ|こんばんわ|ちーす|チース|Hello|Hi)'),
	re.compile('占'),
	re.compile('ぬるぽ'),
	re.compile('status')]
	
TRIGGER_ACTION = [
	'ADD_EVENT',
	'ADD_EVENT',
	'TELL_EVENT',
	'TELL_EVENT_HELP',
	'GREET',
	'TELL_FORTUNE',
	'NULL_POINTER',
	'TELL_STATUS']
	
# Messages

MESSAGE = {
	'EVENT': {
		'NOIDEA' : u'予定の登録ですか？「16時から17時までGrandeで会議」といった形でお伝え下さい！',
		'TRY' : u'予定の登録を行ってみます。',
		'CHECK_AVAIL' : u'%sの空きを確認しています',
		'RESOURCE_BUSY' : u'%sには空きがありません',
		'FAILED' : u'予定の登録に失敗しました。時間をおいて再度お試し下さい…。',
		'SUCCESS' : u'%d時から%d時まで、「%s」と登録しておきました。'
	},
	'FORTUNE': [
		u'注意力が散漫になりそうな一日。今日は早めに帰ってのんびりしてみては？',
		u'アイデアがよく浮かびそうな日。新しい提案をしてみるチャンスです。',
		u'つい気持ちが大きくなりそうな日。時々自分の態度を確認してみて',
		u'思い切った行動にでると発見がありそう。パソコン内のファイル整理でもしてみては？',
		u'昔からの人脈に助けられそうな日。お歳暮はサラダ油が吉',
		u'新規顧客が増えそうな日。思い切って予定を入れてみよう！ http://b-rakumo.appspot.com/contacts',
		u'ポカポカ陽気に上司の財布もゆるみがち。こっそりマシンの購入申請通しちゃえ！ http://b-rakumo.appspot.com/workflow'
	],
	'GREET': [
		u'こんにちわ、%sさん！',
		u'おひさしぶりです、%sさん！',
		u'お疲れ様です、%sさん',
		u'あ、%sさん…',
		u'あぁ%sさん',
		u'%sさん、どうもー',
		u'%sさん、こんにちわ♫',
		u'はい！%sさんなんでしょう？',
		u'%sさんどうしました？'
	],
	'RANDOM' : [
		u'え？',
		u'そうですね',
		u'へー',
		u'ふーん',
		u'日本語でおｋ',
		u'どこを縦読み？',
		u'で？',
		u'ミサワかよｗｗｗ'
	],
	'NULL_POINTER': u'ｶﾞｯ'
}
		

	
	
	
