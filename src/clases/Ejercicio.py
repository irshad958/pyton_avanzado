import logging
import time

import boto3

logging.basicConfig(level=logging.WARNING)


def check_no_tags(d):
    no_tags = []
    for a, i in d.items():
        if i is None:
            no_tags.append(a)

    print('no tags {}'.format(len(no_tags)))


if "__main__" == __name__:
    sqs = boto3.client('sqs')

    # List SQS queues

    t1 = time.time()

    queues = sqs.list_queues()

    print(f"get queues from sqs {t1 - time.time()}")

    t1 = time.time()
    result = {}
    dev_queues = {}
    cl_queues = {}
    mx_queues = {}
    col_queues = {}
    arg_queues = {}
    ec_queues = {}
    es_queues = {}
    br_queues = {}
    pa_queues = {}
    pe_queues = {}

    no_tag_queues = {}
    others_queues = {}

    for i in queues.get('QueueUrls'):
        tags = sqs.list_queue_tags(QueueUrl=i)
        result[i.split('/')[4]] = tags.get('Tags')

    for key, value in result.items():
        if key.find('dev-') == 0:
            dev_queues[key] = value

    for key, value in result.items():
        if key.find('-cl-') != -1 and not (key.find('dev') == 0):
            cl_queues[key] = value

    for key, value in result.items():
        if key.find('-mx-') != -1 and not (key.find('dev') == 0):
            mx_queues[key] = value

    for key, value in result.items():
        if key.find('-col-') != -1 and not (key.find('dev') == 0):
            col_queues[key] = value

    for key, value in result.items():
        if key.find('-arg-') != -1 and not (key.find('dev') == 0):
            arg_queues[key] = value

    for key, value in result.items():
        if key.find('-ec-') != -1 and not (key.find('dev') == 0):
            ec_queues[key] = value

    for key, value in result.items():
        if key.find('-es-') != -1 and not (key.find('dev') == 0):
            es_queues[key] = value

    for key, value in result.items():
        if key.find('-br-') != -1 and not (key.find('dev') == 0):
            br_queues[key] = value

    for key, value in result.items():
        if key.find('-pa-') != -1 and not (key.find('dev') == 0):
            pa_queues[key] = value

    for key, value in result.items():
        if key.find('-pe-') != -1 and not (key.find('dev') == 0):
            pe_queues[key] = value

    for key, value in result.items():
        if value is None:
            no_tag_queues[key] = value

    for key, value in result.items():
        if key.find('-pe-') == -1 \
                and not (key.find('dev-') == 0) \
                and key.find('-ec-') == -1 \
                and key.find('-cl-') == -1 \
                and key.find('-ar-') == -1 \
                and key.find('-br-') == -1 \
                and key.find('-pa-') == -1 \
                and key.find('-es-') == -1 \
                and key.find('-co-') == -1 \
                and key.find('-mx-') == -1:
            others_queues[key] = value

    print(f" processing time =  {t1 - time.time()}")

    print("Total {}".format(len(result)))

    print("devs {}".format(len(dev_queues)))
    check_no_tags(dev_queues)

    print("CL {}".format(len(cl_queues)))
    check_no_tags(cl_queues)

    print("AR {}".format(len(arg_queues)))
    check_no_tags(arg_queues)

    print("COL {}".format(len(col_queues)))
    check_no_tags(col_queues)

    print("EC {}".format(len(ec_queues)))
    check_no_tags(ec_queues)

    print("EEUU {}".format(len(es_queues)))
    check_no_tags(es_queues)
    print("BR {}".format(len(br_queues)))
    check_no_tags(br_queues)

    print("MX {}".format(len(mx_queues)))
    check_no_tags(mx_queues)

    print("PE {}".format(len(pe_queues)))
    check_no_tags(pe_queues)

    print("PA {}".format(len(pa_queues)))
    check_no_tags(pa_queues)

    print("others {}".format(len(others_queues)))
    check_no_tags(others_queues)

    print("Without tags {}".format(len(no_tag_queues)))

    print("all = {} ".format(
        (len(dev_queues) + len(cl_queues)) + len(arg_queues) + len(col_queues) + len(ec_queues) + len(es_queues) + len(
            br_queues) + len(mx_queues) + len(pe_queues) + len(pa_queues) + len(others_queues)))
