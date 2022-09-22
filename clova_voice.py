# 네이버 음성합성 Open API 예제
import os
import datetime
import urllib.request
from dataclasses import dataclass
from rich.pretty import pprint as print
from dotenv import load_dotenv
load_dotenv()

from simple_term_menu import show_menu


def env(key: str, default: str = None, type: type = str):
    if default is None:
        return type(os.environ.get(key))
    else:
        return type(os.environ.get(key, default))


@dataclass
class HeaderConfig:
    client_id = env('client_id')
    client_secret = env('client_secret')
    content_type = env('content_type')


def make_clova_voice_api_data(
    speaker: str,
    text: str, 
    volume: int = 0, 
    speed: int = 0, 
    pitch: int = 0, 
    emotion: int = 0, 
    format: str = 'mp3', 
    sampling_rate: int = 24000
) -> str:
    """
    Parameters
    --------
        `speaker` : `str`- 음성 합성에 사용할 목소리 종류
            사용 가능한 speaker 종류: `print_all_speakers()` 실행하거나 하단 See Also 참고
            
        `text` : `str` - 음성 합성할 문장
            UTF-8 인코딩된 텍스트만 지원
            최대 2,000 자의 텍스트까지 음성 합성을 지원
            기호나 괄호 안의 텍스트는 읽지 않음	없음
    
        `volume` `int` - 음성 볼륨
            -5에서 5 사이의 정수 값이며, -5 이면 0.5 배 낮은 볼륨이고 5 이면 1.5 배 더 큰 볼륨
            0 이면 정상 볼륨의 목소리로 음성을 합성함
            >>> -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5
    
        `speed`	`int` - 음성 속도
            -5에서 5 사이의 정수 값이며, -5 이면 2 배 빠른 속도이고 5 이면 0.5 배 더 느린 속도
            0 이면 정상 속도의 목소리로 음성을 합성함
            >>> -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5
    
        `pitch`	`int` - 음성 피치
            -5에서 5 사이의 정수 값이며, -5 이면 1.2 배 높은 피치이고 5 이면 0.8 배 더 낮은 피치
            0 이면 정상 피치의 목소리로 음성을 합성함
            >>> -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5
    
        `emotion` `int` - 음성 감정
            0에서 2 사이의 정수 값이며 0 은 기본, 1 은 어두운, 2 는 밝은 음성임 (nara만 사용 가능)
            >>> 0, 1, 2
    
        `format` `str` - 음성 포멧
            mp3 또는 wav 입력 바람
            >>> 'mp3', 'wav'
        
        `sampling_rate`	`int` - sampling rate. sampling rate 는 wav 포멧만 지원됨
            >>> 8000, 16000, 24000, 48000

    Returns
    --------
    'data' 'str'
    See Also
    --------
        사용 가능한 `speaker` parameter 종류
        >>> speakers = [
            ('nara', '아라', '한국어', '여성 음색'),
            ('nara_call', '아라(상담원)', '한국어', '여성 음색'),
            ('nminyoung', '민영', '한국어', '여성 음색'),
            ('nyejin', '예진', '한국어', '여성 음색'),
            ('mijin', '미진', '한국어', '여성 음색'),
            ('jinho', '진호', '한국어', '남성 음색'),
            ('clara', '클라라', '영어', '여성 음색'),
            ('matt', '매트', '영어', '남성 음색'),
            ('shinji', '신지', '일본어', '남성 음색'),
            ('meimei', '메이메이', '중국어', '여성 음색'),
            ('liangliang', '량량', '중국어', '남성 음색'),
            ('jose', '호세', '스페인어', '남성 음색'),
            ('carmen', '카르멘', '스페인어', '여성 음색'),
            ('nminsang', '민상', '한국어', '남성 음색'),
            ('nsinu', '신우', '한국어', '남성 음색'),
            ('nhajun', '하준', '한국어', '아동 음색 (남)'),
            ('ndain', '다인', '한국어', '아동 음색 (여)'),
            ('njiyun', '지윤', '한국어', '여성 음색'),
            ('nsujin', '수진', '한국어', '여성 음색'),
            ('njinho', '진호', '한국어', '남성 음색'),
            ('njihun', '지훈', '한국어', '남성 음색'),
            ('njooahn', '주안', '한국어', '남성 음색'),
            ('nseonghoon', '성훈', '한국어', '남성 음색'),
            ('njihwan', '지환', '한국어', '남성 음색'),
            ('nsiyoon', '시윤', '한국어', '남성 음색'),
            ('ngaram', '가람', '한국어', '아동 음색 (여)'),
            ('ntomoko', '토모코', '일본어', '여성 음색'),
            ('nnaomi', '나오미', '일본어', '여성 음색'),
            ('dnaomi_joyful', '나오미(기쁨)', '일본어', '여성 음색'),
            ('dnaomi_formal', '나오미(뉴스)', '일본어', '여성 음색'),
            ('driko', '리코', '일본어', '여성 음색'),
            ('deriko', '에리코', '일본어', '여성 음색'),
            ('nsayuri', '사유리', '일본어', '여성 음색'),
            ('ngoeun', '고은', '한국어', '여성 음색'),
            ('neunyoung', '은영', '한국어', '여성 음색'),
            ('nsunkyung', '선경', '한국어', '여성 음색'),
            ('nyujin', '유진', '한국어', '여성 음색'),
            ('ntaejin', '태진', '한국어', '남성 음색'),
            ('nyoungil', '영일', '한국어', '남성 음색'),
            ('nseungpyo', '승표', '한국어', '남성 음색'),
            ('nwontak', '원탁', '한국어', '남성 음색'),
            ('dara_ang', '아라(화남)', '한국어', '여성 음색'),
            ('nsunhee', '선희', '한국어', '여성 음색'),
            ('nminseo', '민서', '한국어', '여성 음색'),
            ('njiwon', '지원', '한국어', '여성 음색'),
            ('nbora', '보라', '한국어', '여성 음색'),
            ('njonghyun', '종현', '한국어', '남성 음색'),
            ('njoonyoung', '준영', '한국어', '남성 음색'),
            ('njaewook', '재욱', '한국어', '남성 음색'),
            ('danna', '안나', '영어', '여성 음색'),
            ('djoey', '조이', '영어', '여성 음색'),
            ('dhajime', '하지메', '일본어', '남성 음색'),
            ('ddaiki', '다이키', '일본어', '남성 음색'),
            ('dayumu', '아유무', '일본어', '남성 음색'),
            ('dmio', '미오', '일본어', '여성 음색'),
            ('chiahua', '차화', '대만어', '여성 음색'),
            ('kuanlin', '관린', '대만어', '남성 음색'),
            ('nes_c_hyeri', '혜리', '한국어', '여성 음색'),
            ('nes_c_sohyun', '소현', '한국어', '여성 음색'),
            ('nes_c_mikyung', '미경', '한국어', '여성 음색'),
            ('nes_c_kihyo', '기효', '한국어', '남성 음색'),
            ('ntiffany', '기서', '한국어', '여성 음색'),
            ('napple', '늘봄', '한국어', '여성 음색'),
            ('njangj', '드림', '한국어', '여성 음색'),
            ('noyj', '봄달', '한국어', '여성 음색'),
            ('neunseo', '은서', '한국어', '여성 음색'),
            ('nheera', '희라', '한국어', '여성 음색'),
            ('nyoungmi', '영미', '한국어', '여성 음색'),
            ('nnarae', '나래', '한국어', '여성 음색'),
            ('nyeji', '예지', '한국어', '여성 음색'),
            ('nyuna', '유나', '한국어', '여성 음색'),
            ('nkyunglee', '경리', '한국어', '여성 음색'),
            ('nminjeong', '민정', '한국어', '여성 음색'),
            ('nihyun', '이현', '한국어', '여성 음색'),
            ('nraewon', '래원', '한국어', '남성 음색'),
            ('nkyuwon', '규원', '한국어', '남성 음색'),
            ('nkitae', '기태', '한국어', '남성 음색'),
            ('neunwoo', '은우', '한국어', '남성 음색'),
            ('nkyungtae', '경태', '한국어', '남성 음색'),
            ('nwoosik', '우식', '한국어', '남성 음색'),
        ]
    Notes
    --------
    Examples
    --------

    """
    
    # text = urllib.parse.quote(text)

    data = f'speaker={speaker}&volume={volume}&speed={speed}&pitch={pitch}&emotion={emotion}&format={format}&sampling_rate={sampling_rate}&text={text}'
    
    return data


def request_clova_voice_api(
    data: str,
    config: HeaderConfig,
    format: str,
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts",
):
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", config.client_id)
    request.add_header("X-NCP-APIGW-API-KEY", config.client_secret)
    request.add_header("Content-Type", config.content_type)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if rescode == 200:
        filename = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        print(f'TTS {filename}.{format} 저장')
        response_body = response.read()

        os.makedirs('save', exist_ok=True)
        with open(f'save/{filename}.{format}', 'wb') as f:
            f.write(response_body)
    else:
        print('Error Code:' + rescode)


def print_all_speakers():
    speakers = [
        ('nara', '아라', '한국어', '여성 음색'),
        ('nara_call', '아라(상담원)', '한국어', '여성 음색'),
        ('nminyoung', '민영', '한국어', '여성 음색'),
        ('nyejin', '예진', '한국어', '여성 음색'),
        ('mijin', '미진', '한국어', '여성 음색'),
        ('jinho', '진호', '한국어', '남성 음색'),
        ('clara', '클라라', '영어', '여성 음색'),
        ('matt', '매트', '영어', '남성 음색'),
        ('shinji', '신지', '일본어', '남성 음색'),
        ('meimei', '메이메이', '중국어', '여성 음색'),
        ('liangliang', '량량', '중국어', '남성 음색'),
        ('jose', '호세', '스페인어', '남성 음색'),
        ('carmen', '카르멘', '스페인어', '여성 음색'),
        ('nminsang', '민상', '한국어', '남성 음색'),
        ('nsinu', '신우', '한국어', '남성 음색'),
        ('nhajun', '하준', '한국어', '아동 음색 (남)'),
        ('ndain', '다인', '한국어', '아동 음색 (여)'),
        ('njiyun', '지윤', '한국어', '여성 음색'),
        ('nsujin', '수진', '한국어', '여성 음색'),
        ('njinho', '진호', '한국어', '남성 음색'),
        ('njihun', '지훈', '한국어', '남성 음색'),
        ('njooahn', '주안', '한국어', '남성 음색'),
        ('nseonghoon', '성훈', '한국어', '남성 음색'),
        ('njihwan', '지환', '한국어', '남성 음색'),
        ('nsiyoon', '시윤', '한국어', '남성 음색'),
        ('ngaram', '가람', '한국어', '아동 음색 (여)'),
        ('ntomoko', '토모코', '일본어', '여성 음색'),
        ('nnaomi', '나오미', '일본어', '여성 음색'),
        ('dnaomi_joyful', '나오미(기쁨)', '일본어', '여성 음색'),
        ('dnaomi_formal', '나오미(뉴스)', '일본어', '여성 음색'),
        ('driko', '리코', '일본어', '여성 음색'),
        ('deriko', '에리코', '일본어', '여성 음색'),
        ('nsayuri', '사유리', '일본어', '여성 음색'),
        ('ngoeun', '고은', '한국어', '여성 음색'),
        ('neunyoung', '은영', '한국어', '여성 음색'),
        ('nsunkyung', '선경', '한국어', '여성 음색'),
        ('nyujin', '유진', '한국어', '여성 음색'),
        ('ntaejin', '태진', '한국어', '남성 음색'),
        ('nyoungil', '영일', '한국어', '남성 음색'),
        ('nseungpyo', '승표', '한국어', '남성 음색'),
        ('nwontak', '원탁', '한국어', '남성 음색'),
        ('dara_ang', '아라(화남)', '한국어', '여성 음색'),
        ('nsunhee', '선희', '한국어', '여성 음색'),
        ('nminseo', '민서', '한국어', '여성 음색'),
        ('njiwon', '지원', '한국어', '여성 음색'),
        ('nbora', '보라', '한국어', '여성 음색'),
        ('njonghyun', '종현', '한국어', '남성 음색'),
        ('njoonyoung', '준영', '한국어', '남성 음색'),
        ('njaewook', '재욱', '한국어', '남성 음색'),
        ('danna', '안나', '영어', '여성 음색'),
        ('djoey', '조이', '영어', '여성 음색'),
        ('dhajime', '하지메', '일본어', '남성 음색'),
        ('ddaiki', '다이키', '일본어', '남성 음색'),
        ('dayumu', '아유무', '일본어', '남성 음색'),
        ('dmio', '미오', '일본어', '여성 음색'),
        ('chiahua', '차화', '대만어', '여성 음색'),
        ('kuanlin', '관린', '대만어', '남성 음색'),
        ('nes_c_hyeri', '혜리', '한국어', '여성 음색'),
        ('nes_c_sohyun', '소현', '한국어', '여성 음색'),
        ('nes_c_mikyung', '미경', '한국어', '여성 음색'),
        ('nes_c_kihyo', '기효', '한국어', '남성 음색'),
        ('ntiffany', '기서', '한국어', '여성 음색'),
        ('napple', '늘봄', '한국어', '여성 음색'),
        ('njangj', '드림', '한국어', '여성 음색'),
        ('noyj', '봄달', '한국어', '여성 음색'),
        ('neunseo', '은서', '한국어', '여성 음색'),
        ('nheera', '희라', '한국어', '여성 음색'),
        ('nyoungmi', '영미', '한국어', '여성 음색'),
        ('nnarae', '나래', '한국어', '여성 음색'),
        ('nyeji', '예지', '한국어', '여성 음색'),
        ('nyuna', '유나', '한국어', '여성 음색'),
        ('nkyunglee', '경리', '한국어', '여성 음색'),
        ('nminjeong', '민정', '한국어', '여성 음색'),
        ('nihyun', '이현', '한국어', '여성 음색'),
        ('nraewon', '래원', '한국어', '남성 음색'),
        ('nkyuwon', '규원', '한국어', '남성 음색'),
        ('nkitae', '기태', '한국어', '남성 음색'),
        ('neunwoo', '은우', '한국어', '남성 음색'),
        ('nkyungtae', '경태', '한국어', '남성 음색'),
        ('nwoosik', '우식', '한국어', '남성 음색'),
    ]
    speakers_dict = {}
    for name, name_ko, lang, gender in speakers:
        if speakers_dict.get(lang) is None:
            speakers_dict[lang] = {}
        if speakers_dict.get(lang).get(gender) is None:
            speakers_dict[lang][gender] = []
        speakers_dict[lang][gender].append(f'{name} ({name_ko})')

    print(speakers_dict, expand_all=True)


if __name__ == '__main__':
    # print_all_speakers()

    filename = env('text_file')
    
    with open(filename, 'r', encoding='UTF-8') as f:
        text = f.read()

    data_kwargs = {
        'speaker': env('speaker'),
        'text': text,
        'volume': env('volume', 0, int),
        'speed': env('speed', 0, int),
        'pitch': env('pitch', 0, int),
        'emotion': env('emotion', 0, int),
        'format': env('format', 'mp3'),
        'sampling_rate': env('sampling_rate', 24000, int),
    }
    print(data_kwargs)

    proceed, choice = show_menu({'[1]Yes': True, '[0]No': False}, title='계속 진행하시겠습니까?')

    if proceed:
        data = make_clova_voice_api_data(**data_kwargs)
        request_clova_voice_api(data, HeaderConfig, data_kwargs['format'])
    else:
        print('API 요청이 취소됐습니다')
