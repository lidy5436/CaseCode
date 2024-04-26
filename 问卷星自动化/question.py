import random
import time

import numpy.random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

# 填空题参数
texts = {}
# 填空题概率参数
textsProb = {}
# 单选题参数
singleProb = {}
# 多选题参数
multipleProb = {}
# 量表题概率参数
scaleProb = {}
# 下拉框概率
dropDownProb = {}


# 检测题量和页数
# 返回结果: 数组 ['第一页题数','第二页题数','第三页题数',...]
def selectQuestionNumAndPage(driver):
    questionList = []
    xpath = '//*[@id="divQuestion"]/fieldset'
    # 页数
    pageNum = len(driver.find_elements(By.XPATH, xpath))
    # 每一页的题
    questions = driver.find_elements(By.XPATH, f'//*[@id="fieldset1"]/div')
    # 无效问题数量
    invalidQuestionNum = 0
    for item in questions:
        if item.get_attribute('topic').isdigit() is False:
            invalidQuestionNum += 1
    # 如果只有一页
    questionList.append(len(questions) - invalidQuestionNum)
    if pageNum >= 2:
        for i in range(2, pageNum + 1):
            questions = driver.find_elements(By.XPATH, f'//*[@id="fieldset{i}"]/div')
            invalidQuestionNum = 0
            for item in questions:
                if item.get_attribute('topic').isdigit() is False:
                    invalidQuestionNum += 1
            questionList.append(len(questions) - invalidQuestionNum)
    return questionList


# 刷题逻辑函数
def findAnswers(driver, answer):
    # 获取必要参数
    global texts, textsProb, singleProb, multipleProb, scaleProb, dropDownProb
    texts = answer.get('texts')
    textsProb = answer.get('textsProb')
    singleProb = answer.get('singleProb')
    multipleProb = answer.get('multipleProb')
    scaleProb = answer.get('scaleProb')
    dropDownProb = answer.get('dropDownProb')

    # 获取题目数量
    questionNumList = selectQuestionNumAndPage(driver)
    # 题号
    current = 0
    # 遍历每一页
    for pageNum in questionNumList:
        # 遍历每一道题
        for questionNum in range(1, pageNum + 1):
            current += 1
            # 确定题型
            questionType = driver.find_element(By.CSS_SELECTOR, f'#div{current}').get_attribute('type')
            if questionType == '1' or questionType == '2':
                # 单选题
                vacantQuestion(driver, current)
            elif questionType == '3':
                # 单选题
                singleQuestion(driver, current)
            elif questionType == '4':
                # 多选题
                multipleQuestion(driver, current)
            elif questionType == '5':
                # 量表题
                scaleQuestion(driver, current)
            elif questionType == '6':
                # 矩阵题
                pass
            elif questionType == '7':
                dropDownQuestion(driver, current)
            elif questionType == '8':
                # 滑块题
                sliderQuestion(driver, current)
            elif questionType == '9':
                # 排序题
                orderQuestion(driver, current)
            else:
                print(f"第{questionNum}题为不支持题型！")
        time.sleep(0.5)
        # 点击下一页
        try:
            driver.find_element(By.CSS_SELECTOR, '#divNext').click()
            time.sleep(0.5)
        except:
            # 点击提交
            driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    submitQuestion(driver)


# 提交问卷
def submitQuestion(driver):
    time.sleep(1)
    # 点击对话框的确认按钮
    try:
        driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
        time.sleep(1)
    except:
        pass
    # 点击智能检测按钮
    try:
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(1)
    except:
        pass
    # 滑块验证
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith('请按住滑块'):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
    except:
        pass


# 填空题
def vacantQuestion(driver, current):
    context = texts.get(str(current))
    prob = textsProb.get(str(current))
    prob = [x / sum(prob) for x in prob]
    textIndex = numpy.random.choice(a=numpy.arange(0, len(prob)), p=prob)
    driver.find_element(By.CSS_SELECTOR, f'#q{current}').send_keys(context[textIndex])


# 单选题
def singleQuestion(driver, current):
    xpath = f'//*[@id="div{current}"]/div[2]/div'
    options = driver.find_elements(By.XPATH, xpath)
    prob = singleProb.get(str(current))
    if prob is None:
        option = random.randint(1, len(options))
    else:
        if len(prob) != len(options):
            print(f"第{current}题参数数量：{len(prob)},选项数量{len(options)},不一致！")
            return
        prob = [x / sum(prob) for x in prob]
        option = numpy.random.choice(a=numpy.arange(1, len(options) + 1), p=prob)
    driver.find_element(By.CSS_SELECTOR,
                        f'#div{current} > div.ui-controlgroup > div:nth-child({option})').click()


# 多选题
def multipleQuestion(driver, current):
    xpath = f'//*[@id="div{current}"]/div[2]/div'
    options = driver.find_elements(By.XPATH, xpath)
    multipleList = []
    prob = multipleProb.get(str(current))
    if len(options) != len(prob):
        print(f"第{current}题概率值和选项值不一致")
        return
        # 生成序列，同时保证至少有一个
    while sum(multipleList) <= 1:
        multipleList = []
        for item in prob:
            option = numpy.random.choice(a=numpy.arange(0, 2), p=[1 - (item / 100), item / 100])
            multipleList.append(option)
    # 依次点击
    for (index, item) in enumerate(multipleList):
        if item == 1:
            css = f"#div{current} > div.ui-controlgroup > div:nth-child({index + 1})"
            driver.find_element(By.CSS_SELECTOR, css).click()


# 量表题
def scaleQuestion(driver, current):
    xpath = f'//*[@id="div{current}"]/div[2]/div/ul/li'
    options = driver.find_elements(By.XPATH, xpath)
    prob = scaleProb.get(str(current))
    if prob is None:
        option = random.randint(1, len(options))
    else:
        prob = [x / sum(prob) for x in prob]
        option = numpy.random.choice(a=numpy.arange(1, len(options) + 1), p=prob)
    driver.find_element(By.CSS_SELECTOR,
                        f"#div{current} > div.scale-div > div > ul > li:nth-child({option})").click()


# 下拉选择题
def dropDownQuestion(driver, current):
    # 先点击 '请选择'
    driver.find_element(By.CSS_SELECTOR, f"#select2-q{current}-container").click()
    time.sleep(0.5)
    # 选项数量
    options = driver.find_elements(By.XPATH, f"//*[@id='select2-q{current}-results']/li")
    prob = dropDownProb.get(str(current))
    prob = [x / sum(prob) for x in prob]
    option = numpy.random.choice(a=numpy.arange(1, len(options)), p=prob)
    driver.find_element(By.XPATH, f"//*[@id='select2-q{current}-results']/li[{option + 1}]").click()


# 滑块题
def sliderQuestion(driver, current):
    scope = random.randint(1, 100)
    driver.find_element(By.CSS_SELECTOR, f'#q{current}').send_keys(scope)


# 排序题
def orderQuestion(driver, current):
    xpath = f'//*[@id="div{current}"]/ul/li'
    options = driver.find_elements(By.XPATH, xpath)
    for i in range(1, len(options) + 1):
        option = random.randint(i, len(options))
        driver.find_element(By.CSS_SELECTOR, f'#div{current} > ul > li:nth-child({option})').click()
        time.sleep(0.4)
