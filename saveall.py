from selenium import webdriver
import time
import csv
import os

path = "C:/Users/intel/chromedriver/driver/chromedriver.exe"

def getLearningPath():
    #options = Options()
    # options.headless = True
    driver = webdriver.Chrome(executable_path = path)


    driver.get('https://www.lynda.com/portal/sip?org=houstonlibrary.org&triedlogout=true')
    time.sleep(3)
    driver.find_element_by_id('card-number').send_keys('2536871')
    time.sleep(2)
    driver.find_element_by_id('card-pin').send_keys('0962')
    time.sleep(2)
    driver.find_element_by_id('submit-library-card').click()
    time.sleep(2)

    driver.get('https://www.lynda.com/learning-paths')
    soup = driver.find_element_by_class_name('tab-content')

    tab_pannel = soup.find_elements_by_class_name('tab-pane')

    for tab in tab_pannel:
        time.sleep(2)

        ul = tab.find_element_by_tag_name('ul')
        lists = ul.find_elements_by_tag_name('li')

        for i in lists:
            url = i.find_element_by_tag_name('a').get_attribute('href')
            with open('link.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([str(url)])

    del driver
    print('Driver Destroyed!')
    #getVideoPages()


def getVideoPages():
    #options = Options()
# options.headless = True
    driver = webdriver.Chrome(executable_path = path)


    driver.get('https://www.lynda.com/portal/sip?org=houstonlibrary.org&triedlogout=true')
    time.sleep(3)
    driver.find_element_by_id('card-number').send_keys('2536871')
    time.sleep(2)
    driver.find_element_by_id('card-pin').send_keys('0962')
    time.sleep(2)
    driver.find_element_by_id('submit-library-card').click()
    time.sleep(2)
    with open('link.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        lp = 0
        for row in csv_reader:
            lp += 1
            if row[0] == 'https://www.lynda.com/learning-paths/Design/working-with-creatives':
                continue
            driver.get(row[0])
            time.sleep(2)
            container = driver.find_element_by_id('path-header')
            try:
                start = container.find_element_by_class_name('hero-cta')
            except:
                print('except')
                path_courses = driver.find_element_by_class_name('path-courses')
            else:
                print('else')
                time.sleep(3)
                start.find_element_by_tag_name('button').click()
                time.sleep(3)
                modal = driver.find_element_by_id('focus-modal')
                dialog = modal.find_element_by_class_name('modal-dialog')
                dialog.find_elements_by_class_name('btn')[1].click()
                time.sleep(5)
                driver.get(row[0])
                time.sleep(2)
                path_courses = driver.find_element_by_class_name('path-courses')
            finally:
                print('finally')
                time.sleep(2)
                container = path_courses.find_element_by_class_name('container')
                path_list = container.find_element_by_class_name('path-list')

                rows = path_list.find_elements_by_class_name('item-details')
                for i in rows:
                    with open('courses.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        ''' it will save title and link of course '''
                        title = i.find_element_by_tag_name('h2').get_attribute('innerHTML')
                        title = (title[0: title.find('<')]).strip()
                        link = i.find_element_by_tag_name('a').get_attribute('href')
                        writer.writerow([str(title),str(link)])
            #del container
            #print(lp)
    del driver
    print('Driver Destroyed!')
    #coursePage()



''' It will scrape all the general information about the course, like Author, Release Data,
SkillLevel, Duration, Viewers etc.'''

courses_info = []

def coursePage():
    #options = Options()
# options.headless = True
    driver = webdriver.Chrome(executable_path = path)


    driver.get('https://www.lynda.com/portal/sip?org=houstonlibrary.org&triedlogout=true')
    time.sleep(3)
    driver.find_element_by_id('card-number').send_keys('2536871')
    time.sleep(2)
    driver.find_element_by_id('card-pin').send_keys('0962')
    time.sleep(2)
    driver.find_element_by_id('submit-library-card').click()
    time.sleep(2)
    fields = ['Course Name' , 'Course Link' ,'Author' ,'Release Date' , 'Duration' , 'Skill Level' , 'Number of Viewers']
    with open('courses.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        writer = csv.writer(csv_file)
        for row in csv_reader:


            driver.get(row[1])


            container = driver.find_element_by_class_name('tab-container')
            time.sleep(2)
            author_thumb = container.find_element_by_class_name('author-thumb')
            author= author_thumb.find_element_by_tag_name('cite').text
            print(f"Author ------> {author}")

            course_desc = container.find_element_by_class_name('course-description')
            release_date = course_desc.find_element_by_tag_name('span').text
            print( f"Release Date ----------> {release_date}")

            #description = course_desc.find_element_by_css_selector('div[itemprop="description"]').text

            skill_level_cont = driver.find_element_by_class_name('course-info-stat-cont')

            skill = skill_level_cont.find_element_by_tag_name('strong').text

            print(f"Skill -----> {skill}")

            duration_cont = driver.find_element_by_class_name('duration')
            duration = duration_cont.find_element_by_tag_name('span').text
            print(f"Duration -----> {duration}")

            viewers_cont = driver.find_element_by_class_name('viewers')
            viewers = viewers_cont.find_element_by_tag_name('span').text
            print(f"Viewers -----> {viewers}")

            course = []
            course.append(row[0])
            course.append(row[1])
            course.append(author)
            course.append(release_date)
            course.append(duration)
            course.append(skill)
            course.append(viewers)

            courses_info.append(course)


            ''' Here, the script will scrape all the links of every video in the course and
            their respective transcripts also'''

            course_toc = driver.find_element_by_class_name('course-toc')

            presentation = course_toc.find_elements_by_css_selector('li[role="presentation"]')
            for i in presentation:

                titles = i.find_elements_by_class_name('chapter-row')
                videos_dict = {
                               'Course-Name' : row[0] ,
                               'Data' : [ {'Section-Name' : '' , 'Links' : [{'VideoName' : '' , 'Link' : '' , 'Transcript' : ''}]} ]}
                for title in titles:

                    ''' main folder  '''
                    Sub_Folder = title.find_element_by_tag_name("h4").text
                    videos_dict['Data'][0]['Section-Name'] = Sub_Folder
                    videos = i.find_elements_by_class_name('video-row')
                    for video in videos:

                        video_name = video.find_element_by_class_name('video-name-cont')
                        video_name.find_element_by_tag_name('a').click()
                        ''' video name '''
                        Video_Name = video_name.find_element_by_tag_name("a").text
                        videos_dict['Data'][0]['Links'][0]['VideoName'] = Video_Name
                        time.sleep(4)
                        ''' Video link '''
                        video_link = driver.find_element_by_tag_name('video').get_attribute('src')
                        videos_dict['Data'][0]['Links'][0]['Link'] = video_link
                        transcript_items = driver.find_element_by_class_name('transcript-items')
                        video_item = transcript_items.find_element_by_class_name('toc-video-item')
                        transcript_cont = video_item.find_element_by_class_name('video-transcript-cont')

                        ps = transcript_cont.find_elements_by_tag_name('p')
                        text = ''
                        for p in ps:
                            spans = p.find_elements_by_tag_name('span')
                            for span in spans:
                                text += span.text
                        videos_dict['Data'][0]['Links'][0]['Transcript'] = text
                        with open('CourseVideos.txt' , 'a' ,encoding = 'utf-8') as vfile:
                            vfile.write(str(videos_dict) + '\n')
            
            file_exists = os.path.isfile("coursesinfo.csv")
            with open('coursesinfo.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file , fieldnames = fields)
                if not file_exists:
                    writer.writeheader()
                
                for cour in courses_info:
                    writer.writerow({'Course Name' : cour[0] , 'Course Link' : cour[1] , 'Author' : cour[2] , 'Release Date' : cour[3] , 'Duration' : cour[4] , 'Skill Level' : cour[5] , 'Number of Viewers' : cour[6]} )
        
    del driver
    print('Driver Destroyed!')




'''Fetch All Paths to All the Categories : getLearningPath(). It will save data to link.csv'''
getLearningPath()
time.sleep(5)
'''Visit Each Category and Fetch all Courses Links : getVideoPages(). It will save data to courses.csv'''
getVideoPages()
time.sleep(5)
'''Visit Each of 3099 course pages and fetch their informations with the links to all the videos : coursePage()
It will save final data to coursesinfo.csv'''
coursePage()
#
#

