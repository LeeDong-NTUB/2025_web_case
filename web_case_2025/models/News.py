from datetime import datetime  # 修正這一行
from django.db import models

class News(models.Model):
    category = models.CharField(max_length=50, blank=False)
    title = models.CharField(max_length=100, blank=False)
    summary = models.TextField(blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField(blank=False)
    
    class Meta:
        app_label = 'bakery_app'

    @staticmethod
    def extract_year_month(date_string):
        """
        從ISO格式的日期字串中提取年份和月份
        
        參數:
            date_string (str): ISO格式的日期字串，如 "2025-04-25T09:30:00"
            
        返回:
            tuple: 包含年份(str)和月份(str)的元組，月份格式為兩位數
        """
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
            year = str(date_obj.year)
            month = f"{date_obj.month:02d}"
            return year, month
        except ValueError:
            # 如果日期格式不正確，返回空值
            return None, None
    
    @staticmethod
    def process_news_data(news_items):
        """
        處理新聞列表，為每個項目添加年份和月份，
        過濾掉未來的新聞，並按年份和月份降序排序
        
        參數:
            news_items (list): 包含新聞項目的列表
            
        返回:
            list: 處理後的新聞列表
        """
        # 處理年份和月份
        for i, item in enumerate(news_items):
            if 'release_date' in item and 'year' not in item and 'month' not in item:
                year, month = News.extract_year_month(item['release_date'])
                if year and month:
                    news_items[i]['year'] = year
                    news_items[i]['month'] = month
        
        # 獲取當前日期
        current_date = datetime.now()
        
        # 過濾掉未來的新聞
        filtered_news = []
        for news in news_items:
            try:
                release_date = datetime.strptime(news['release_date'].split('T')[0], '%Y-%m-%d')
                if release_date <= current_date:
                    filtered_news.append(news)
            except (ValueError, TypeError):
                # 如果日期格式不正確，仍然保留該新聞
                filtered_news.append(news)

        # 按年份和月份排序 (降序)
        filtered_news.sort(key=lambda x: (int(x.get('year', 0)), int(x.get('month', 0))), reverse=True)
        
        return filtered_news