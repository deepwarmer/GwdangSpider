import csv,sys,json,logging
import mail,scrawl
from dw_common_lib import dict_to_object
keys=[]
data=[]
def read_data(filename:str):
    with open(filename)as fin:
        reader=csv.reader(fin)
        keys.extend(reader.__next__())
        data.extend([row for row in reader])
def write_data(filename:str):
    with open(filename,"w")as fout:
        writer=csv.writer(fout)
        writer.writerow(keys)
        writer.writerows(data)
def deal_item(item_info):
    # get items
    new_item=old_item={key:value for key,value in zip(keys,item_info)}
    logging.info(new_item['title']+" is in dealt: "+new_item['product_url'])
    logging.debug("new_item:"+str(new_item))
    #get scrawl result
    parser=scrawl.generate_parser()
    args=parser.parse_args(("-d 180 -s lowest -s highest -s current -s make_up_lowest -s title -s price_url "+new_item['product_url']).split(' '))
    try:
        res=scrawl.scrawl(args)
    except:
        logging.warn("can't scrawl "+new_item['title']+":"+ new_item['product_url'])
        with open("email_config.json") as fin:
            email_config=json.load(fin)
        logging.debug(email_config)
        email_config['subject']="[gwdang scrawler]Can't scrawl "+new_item['title']
        email_config['message']="The product_url is "+new_item['product_url']+'\n'+"do go to deal with it"
        mail.mail(dict_to_object(email_config))
        raise

    logging.debug(res)
    for key in res.keys():new_item[key]=res[key]
    #decide whether to send email
    express=new_item['notification_condition']
    old_substring_list=['OH','OL','OM','OC','NH','NL','NM','NC']
    new_substring_list=[old_item['highest'],old_item['lowest'],old_item['make_up_lowest'],old_item['current'],new_item['highest'],new_item['lowest'],new_item['make_up_lowest']]
    for old_substring,new_substring in zip(old_substring_list,new_substring_list):
        express=express.replace(old_substring,' '+new_substring+' ')
    express=express.replace('  ',' ')
    logging.debug(express)
    whether_to_notify=eval(express)
    
    # send email
    if whether_to_notify:
        with open("email_config.json") as fin:
            email_config=json.load(fin)
        logging.debug(email_config)
        email_config['subject']=f"[gwdang scrawler]{new_item['title']}'s price has changed from {old_item['current']} to {new_item['current']} while lowest is {new_item['lowest']}"
        email_config['message']=json.dumps({"old_item":old_item,"new_item":new_item},ensure_ascii=False,indent=0)
        mail.mail(dict_to_object( email_config))
    #save updated data to data[]
    item_info=list(new_item.values())
    return item_info

if __name__=="__main__":
    logging.basicConfig(stream=sys.stdout,level=logging.INFO)
    read_data("gwdang_product_list.csv")
    for i,item_info in enumerate(data):
        try:
            data[i]=deal_item(item_info)
        except:
            # it has been dealt in deal_item()
            pass

    write_data("gwdang_product_list.csv")    
    

