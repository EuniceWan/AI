from __future__ import print_function
import math
import random


class Bayes_Classifier:

    def __init__(self):

        self.prior_c=0
        self.str_c=''
        self.str_c5=''
        self.word1_num=0
        self.word5_num=0
        self.result_list = []
        self.word_pos_num = []
        self.word_neg_num=[]
        self.word_norepeat=[]
        # dictionary of train_set's classes
        # inside the dict is <word>: [<Positive Count>, <Negative Count>]
        self.class_dict = {}
        self.stoplist = ['a', 'but', 'about', 'by', 'above', 'can', 'after', 'cannot', 'again', 'could', 'against',
                         'couldnt' 'all','did', 'am', 'didnt', 'an', 'do', 'and', 'does', 'any', 'doesn', 't', 'are',
                         'doing', 'aren','don', 'as', 'down','at', 'during', 'be', 'each', 'because', 'few', 'been',
                         'for', 'before', 'from', 'being','further', 'below','had', 'between', 'hadn', 'both', 'has']

    def train(self,filename):
        # code to be completed by students to extract features from training file, and
        # to train naive bayes classifier.

        collection_c=[]
        collection_c5=[]
        sentiment=[]
        review=[]
        field=[]
        nc = 0
        n = 0
        with open(filename, 'rt') as f:
            lines = f.readlines()

        for line in lines:
            line = line.replace('\n', '')
            fields = line.split('|')
            field.append(fields)

            if fields[1] == '1':
                nc=nc+1
                collection_c.append(fields[2].lower())
            else:
                collection_c5.append(fields[2].lower())
            n=n+1


            sentiment.append(int(fields[1]))
            review.append(fields[2])
        self.prior_c = float(nc) / n

        # nc=0
        # n=0
        # for c in sentiment:
        #     if c ==1 :
        #         nc = nc+1
        #     n = n+1
        # # P(pos)
        # self.prior_c= float(nc)/n
        # print (self.prior_c)

        # 6 str_c save pos words
        self.str_c = " ".join(collection_c)
        self.str_c5 = " ".join(collection_c5)
        str_review = " ".join(review)
        # 7 , 8 , 9, 10
        # the num of this word in pos_word

        # num of buchongfu word
        self.word_norepeat = list(set(str_review.split(' ')))
        for word in self.stoplist:
            if word in self.word_norepeat:
                self.word_norepeat.remove(word)

        word_num = len(self.word_norepeat)

        # fenmu
        self.word1_num = word_num + len(self.str_c.split(' '))
        self.word5_num = word_num + len(self.str_c5.split(' '))

        # fenzi
        # t=1
        # t_neg=1
        # for word in self.word_norepeat:
        #     for word1 in self.str_c.split(' '):
        #         if word == word1:
        #
        #             t=t+1
        #
        #     self.word_pos_num.append(t)
        #     t=1
        #     for word_5 in self.str_c5.split(' '):
        #         if word == word_5:
        #             t_neg +=1
        #     self.word_neg_num.append(t_neg)
        #     t_neg=1

        pos_dict = {}
        for word in self.str_c.split(' '):
            if not pos_dict.has_key(word):
                pos_dict[word] = 1
            else:
                pos_dict[word] += 1

        # Then, build up a dict for negative dict also
        neg_dict = {}
        for word in self.str_c5.split(' '):
            if not neg_dict.has_key(word):
                neg_dict[word] = 1
            else:
                neg_dict[word] += 1

        # Build class dict
        for word in self.word_norepeat:
            # If we do not have this word in the dict, create one first
            if not self.class_dict.has_key(word):
                self.class_dict[word] = [1, 1]
            # If it's in positive word dictionary, count
            if word in pos_dict:
                self.class_dict[word][0] += pos_dict[word]
            # If it's in negative word dictionary, count
            if word in neg_dict:
                self.class_dict[word][1] += neg_dict[word]

        for word in self.word_norepeat:
            self.word_pos_num.append(self.class_dict[word][0])
            self.word_neg_num.append(self.class_dict[word][1])



    def classify(self,filename):
        # code to be completed by student to classifier reviews in file using naive bayes
        # classifier previously trains.  member function must return a list of predicted
        # classes with '5' = positive and '1' = negative

        with open(filename, 'rt') as f:
            lines = f.readlines()
        for line in lines:
            # print (123)
            line = line.replace('\n', '')
            fields = line.split('|')
            review = fields[2].lower().split(' ')
            #for word in review:

            p_final1 = math.log(self.prior_c)
            p_final5 = math.log(1 - self.prior_c)

            for word in review:
                if word in self.stoplist:
                    review.remove(word)
            for word_o in review:
                if word_o in self.word_norepeat:
                    index = self.word_norepeat.index(word_o)
                    p_pos_1 = self.word_pos_num[index]/ float(self.word1_num)
                    p_neg_5 = self.word_neg_num[index] / float(self.word5_num)
                else:
                    p_pos_1 = 1 / float(self.word1_num)
                    p_neg_5 = 1 / float(self.word5_num)
                p_final1 += math.log(p_pos_1)
                p_final5 += math.log(p_neg_5)

            if p_final1 >= p_final5:
                self.result_list.append('1')
            else:
                self.result_list.append('5')

        print (self.result_list)


        return self.result_list



 #include<iostream>
  #include<cstdio>
  #include<queue>
  #include<cmath>
  #include<cstring>
  using namespace std;
  char a[10001];
  int now;
  int maxn=-1;
 char ans;
 int main() 
 {

     gets(a);
     int l=strlen(a);
     for(int i=0;i<l;i++)
     {
         if(a[i]==a[i+1])
         now++;
         else
         {
             now++;
             if(now>maxn)
             {
                 maxn=now;
                 ans=a[i];
             }
             if((now==maxn) && (a[i] <a[i-1])){
                maxn=now;
                 ans=a[i];
             }
             now=0;    
         }

     }
  vector<char> res;
  for(int i=0;i<maxn;i++){
      res.add(ans);
  }
     cout<<res;
     return 0;
 }
 













    
