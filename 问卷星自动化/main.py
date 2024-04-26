import time

from selenium import webdriver
import question

# 问卷星地址
url = 'https://www.wjx.cn/vm/QpIXPFr.aspx# '
# 填空题参数
question.texts = {'3': ['选A', '选B', '选C']}
# 填空题概率参数
question.textsProb = {'3': [1, 1, 1]}
# 单选题参数
question.singleProb = {'1': [1, 1, 1, 1]}
# 量表题概率参数
question.scaleProb = {'4': [1, 1, 1, 1, 1]}
# 下拉框概率
question.dropDownProb = {'5': [1, 1]}

# 答案
answer = {
    # 填空题参数
    "texts": {'3': ['选A', '选B', '选C']},
    # 填空题概率参数
    "textsProb": {'3': [1, 1, 1]},
    # 单选题参数
    "singleProb": {'1': [1, 1, 1, 1]},
    # 多选题参数
    "multipleProb": {'2': [100, 25, 50, 40]},
    # 量表题概率参数
    "scaleProb": {'4': [1, 1, 1, 1, 1]},
    # 下拉框概率
    "dropDownProb": {'5': [1, 1]}
}


# 获取本地IP地址
def getLocationIpAddress():
    return '127.0.0.1'


def runRequest():
    for i in range(5):
        # 躲避智能检测，将网页中的window.navigator中的webdriver设置为false
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=option)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get:()=>undefined});'
                                })
        # 设置浏览器的大小和位置
        driver.set_window_size(600, 500)
        driver.set_window_position(x=400, y=50)
        # 访问地址
        driver.get(url)
        # 刷题主逻辑
        question.findAnswers(driver, answer)
        time.sleep(2)
        driver.quit()
        print(f'第{i + 1}份填写完成')


if __name__ == "__main__":
    runRequest()
