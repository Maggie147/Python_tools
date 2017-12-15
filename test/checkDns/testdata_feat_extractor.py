import math
from collections import Counter,defaultdict
import numpy as np
from itertools import groupby
#see if a domain is pronunceable using 2-letter Markov Chain
#https://github.com/rrenaud/Gibberish-Detector
import pickle
import gib_detect_train

hmm_prob_threshold = -120
model_data = pickle.load(open('/home/APT/pylib/checkDns/pki/gib_model.pki', 'rb'))
private_tld_file = open('/home/APT/pylib/checkDns/txt/private_tld.txt','r')
private_tld = set(f.strip() for f in private_tld_file)#black list for private tld
private_tld_file.close()

tld_file = open('/home/APT/pylib/checkDns/txt/tld_list.txt','r')
tld_list_file = list(t.strip().strip('.').decode('utf-8') for t in tld_file)#for domain match, add dot as prefix and postfix
tld_file.close()

n_gram_file = open('/home/APT/pylib/checkDns/txt/n_gram_rank_freq.txt','r')
gram_rank_dict = dict()
for i in n_gram_file:
    cat,gram,freq,rank = i.strip().split(',')
    gram_rank_dict[gram]=int(rank)
n_gram_file.close()

feat_dict = dict()
    
#feature extraction
#- bigrams of main domain
#- tld
#- length of main domain
#- entropy of main domain (unigram)

#header = 'ip,tld,entropy,len,norm_entropy,vowel_ratio,digit_ratio,repeat_letter,consec_digit,consec_consonant,gib_value,hmm_log,uni_rank,bi_rank,tri_rank,uni_std,bi_std,tri_std,private_tld,class\n'
#fw.write('%s'%(header))

#pronounce detection
#google true
#baidu true
#123 true
#aaaf false
model_mat = model_data['mat']
threshold = model_data['thresh']

#load trans matrix for bigram markov model
transitions = defaultdict(lambda: defaultdict(float))

f_trans = open('/home/APT/pylib/checkDns/trans_matrix.csv','r')
for f in f_trans:
    key1,key2,value =f.rstrip().split('\t')#key1 can be '' so rstrip() only
    value = float(value)
    transitions[key1][key2]=value

f_trans.close()

def feat_extract(dnslist):
    fw = open('/home/APT/pylib/checkDns/txt/test.txt','w')
    header = 'ip,tld,entropy,len,norm_entropy,vowel_ratio,digit_ratio,repeat_letter,consec_digit,consec_consonant,gib_value,hmm_log,uni_rank,bi_rank,tri_rank,uni_std,bi_std,tri_std,private_tld\n'
    fw.write('%s'%(header))
    print 'start'
    for dns in dnslist:
        domain = dns
        if(len(dns)>4):
            if(dns[0:4]=='www.'):
                domain = dns[4:]
        domain = domain.strip('"')
        strip_domain = domain.strip('.')
        #if not tld=='NONE':
        #    strip_domain = domain[:-len(tld)]
        #strip_domain=strip_domain.strip('.')
        #main_domain = '$'+strip_domain.split('.')[-1]+'$'
        ext = strip_domain
        tld = max_match(ext,tld_list_file)
        if tld:
            main_domain = '$'+ext[0:-(len(tld)+1)]+'$'
        else:
            main_domain = '$'+ext.split('.')[0]+'$'
        if len(main_domain)>4 and main_domain[:4]=='xn--':#remove non-ascii domain
            continue
        hmm_main_domain ='^'+domain.strip('.')+'$' #^ and $ of full domain name for HMM
        has_private_tld = 0
        #check if it is a private tld
        if tld in private_tld:
            has_private_tld = 1
            tld_list = tld.split('.')#quick hack: if private tld, use its last part of top TLD
            tld = tld_list[-1]
            main_domain = '$'+tld_list[-2]+'$'#and overwrite the main domain
        bigram = [''.join(i) for i in bigrams(main_domain)]#extract the bigram
        trigram = [''.join(i) for i in trigrams(main_domain)]#extract the bigram
        f_len = float(len(main_domain))
        count = Counter(i for i in main_domain).most_common()#unigram frequency
        entropy = -sum(j/f_len*(math.log(j/f_len)) for i,j in count)#shannon entropy
        unigram_rank = np.array([gram_rank_dict[i] if i in gram_rank_dict else 0 for i in main_domain[1:-1]])
        bigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in bigrams(main_domain)])#extract the bigram
        trigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in trigrams(main_domain)])#extract the bigram
    
        #linguistic feature: % of vowels, % of digits, % of repeated letter, % consecutive digits and % non-'aeiou'
        vowel_ratio = count_vowels(main_domain)/f_len
        digit_ratio = count_digits(main_domain)/f_len
        repeat_letter = count_repeat_letter(main_domain)/f_len
        consec_digit = consecutive_digits(main_domain)/f_len
        consec_consonant = consecutive_consonant(main_domain)/f_len

        #probability of staying in the markov transition matrix (trained by Alexa)
        hmm_prob_ = hmm_prob(hmm_main_domain)
        if hmm_prob_<math.e**hmm_prob_threshold:#probability is too low to be non-DGA
            hmm_log_prob = -999.
        else:
            hmm_log_prob = math.log(hmm_prob_)

        #advanced linguistic feature: pronouncable domain
        gib_value = int(gib_detect_train.avg_transition_prob(main_domain.strip('$'), model_mat) > threshold)
        try:
            fw.write('%s,%s,%.3f,%.1f,%.3f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%d\n'
                    %(domain,tld,entropy,f_len,entropy/f_len,vowel_ratio,
                    digit_ratio,repeat_letter,consec_digit,consec_consonant,gib_value,hmm_log_prob,
                    ave(unigram_rank),ave(bigram_rank),ave(trigram_rank),
                     std(unigram_rank),std(bigram_rank),std(trigram_rank),
                    has_private_tld)
                    )
        except UnicodeEncodeError:
            continue
    
    return '/home/APT/pylib/checkDns/txt/test.txt'

#while True:
#    l = raw_input()
#    model_mat = model_data['mat']
#    threshold = model_data['thresh']
#    print gib_detect_train.avg_transition_prob(l, model_mat) > threshold
def max_match(domain, tlds):#simple match and find the longest match
   match = [i for i in tlds if i in domain] 
   if len(match)>0:
       for i in sorted(match,key=lambda x: len(x), reverse = True):
           if i == domain[-(len(i)):]:#longest and matches the end of the domain
               return i
   else: return 'NONE'

def ave(array_):#sanity check for NaN
    if len(array_)>0:
        return array_.mean()
    else:
        return 0

def count_vowels(word):#how many a,e,i,o,u
    vowels=list('aeiou')
    return sum(vowels.count(i) for i in word.lower())

def count_digits(word):#how many digits
    digits=list('0123456789')
    return sum(digits.count(i) for i in word.lower())

def count_repeat_letter(word):#how many repeated letter
    count = Counter(i for i in word.lower() if i.isalpha()).most_common()
    cnt = 0
    for letter,ct in count:
        if ct>1:
            cnt+=1
    return cnt

def consecutive_digits(word):#how many consecutive digit
    cnt = 0
    digit_map = [int(i.isdigit()) for i in word]
    consecutive=[(k,len(list(g))) for k, g in groupby(digit_map)]
    count_consecutive = sum(j for i,j in consecutive if j>1 and i==1)
    return count_consecutive

def consecutive_consonant(word):#how many consecutive consonant
    cnt = 0
    #consonant = set(['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z'])
    consonant = set(['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w','x', 'y', 'z'])
    digit_map = [int(i in consonant) for i in word]
    consecutive=[(k,len(list(g))) for k, g in groupby(digit_map)]
    count_consecutive = sum(j for i,j in consecutive if j>1 and i==1)
    return count_consecutive

def std(array_):#sanity check for NaN
    if len(array_)>0:
        return array_.std()
    else:
        return 0

def bigrams(words):
    wprev = None
    for w in words:
        if not wprev==None:
            yield (wprev, w)
        wprev = w

def trigrams(words):
    wprev1 = None
    wprev2 = None
    for w in words:
        if not (wprev1==None or wprev2==None):
            yield (wprev1,wprev2, w)
        wprev1 = wprev2
        wprev2 = w

def hmm_prob(domain):
    bigram = [''.join((i,j)) for i,j in bigrams(domain) if not i==None]
    prob = transitions[''][bigram[0]]
    for x in xrange(len(bigram)-1):
        next_step = transitions[bigram[x]][bigram[x+1]]
        prob*=next_step

    return prob
