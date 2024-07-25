import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np

from django.core.management.base import BaseCommand
from board.models import User, Diary, TodoItem

class Command(BaseCommand):
    help = 'Train the recommendation model'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        diaries = Diary.objects.all()
        todos = TodoItem.objects.all()

        data = {
            'diary': [d.content for d in diaries],
            'todo': [t.task for t in todos],
            'age': [u.age for u in users]
        }

        df = pd.DataFrame(data)

        # 텍스트 데이터 전처리
        vectorizer = TfidfVectorizer()
        diary_tfidf = vectorizer.fit_transform(df['diary'])
        todo_tfidf = vectorizer.fit_transform(df['todo'])

        # 나이 정보 스케일링
        scaler = StandardScaler()
        age_scaled = scaler.fit_transform(df[['age']])

        # 전처리된 데이터 결합
        features = np.hstack((diary_tfidf.toarray(), todo_tfidf.toarray(), age_scaled))

        # 모델 훈련
        model = RandomForestClassifier()
        model.fit(features, df['todo'])

        # 모델 저장
        with open('model.pkl', 'wb') as f:
            pickle.dump((vectorizer, scaler, model), f)

        self.stdout.write(self.style.SUCCESS('Model trained and saved successfully'))
