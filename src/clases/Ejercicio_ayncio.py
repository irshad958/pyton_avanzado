import asyncio
import logging
import time

import aiobotocore
import boto3
import uvloop

logger = logging.getLogger(__name__)


def check_no_tags(d):
    no_tags = []
    for a, i in d.items():
        if i is None:
            no_tags.append(a)

    print('no tags {}'.format(len(no_tags)))


def timming(f):
    def some_function(*args, **kwargs):
        t1 = time.time()
        aux = f(*args, **kwargs)
        print(f"{f.__name__} se demoro {time.time() - t1}")
        return aux

    return some_function


@timming
def get_queue_list(sqs):
    return sqs.list_queues()


def get_queue_by_filter(tags, filter):
    return {key: value for (key, value) in tags if filter(key, value)}


# await release the execution in event loop until the task is complete
# In this case while one process is waiting the response from AWS, another process is able to make an another request.
async def get_queue_tags_async(url, result, io_sqs) -> None:
    tags = await io_sqs.list_queue_tags(QueueUrl=url)
    result[url.split('/')[4]] = tags


# create a generator of executions
def create_invokes(urls, result, sqs):
    for url in urls.get('QueueUrls'):
        yield get_queue_tags_async(url, result, sqs)


# every single method is able to be asynchronous with the async keyword
async def event_loop(queues, result):
    session = aiobotocore.get_session()
    # create a aws session to share with the requests, and also It's asynchronous method
    async with session.create_client('sqs', region_name='sa-east-1', verify=False) as async_sqs:
        invokes = create_invokes(queues, result, async_sqs)
        await asyncio.gather(*invokes)


@timming
def main_async(queues, result):
    # another implementation of event loop engine, It's faster than asyncio implementation, to use the asyncio
    # implementation just comment uvloop.install()
    uvloop.install()
    # asyncio.run execute the event loop, It just casualty the method's name is event_loop :p
    asyncio.run(event_loop(queues, result))


@timming
def main():
    sqs = boto3.client('sqs')

    # List SQS queues

    queues = get_queue_list(sqs)

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

    main_async(queues, result)

    dev_queues = get_queue_by_filter(result.items(), lambda key, value: key.find('dev-') == 0)
    cl_queues = get_queue_by_filter(result.items(),
                                    lambda key, value: key.find('-cl-') != -1 and not (key.find('dev') == 0))

    mx_queues = get_queue_by_filter(result.items(),
                                    lambda key, value: key.find('-mx-') != -1 and not (key.find('dev') == 0))

    col_queues = get_queue_by_filter(result.items(),
                                     lambda key, value: key.find('-co-') != -1 and not (key.find('dev') == 0))

    for key, value in result.items():
        if key.find('-ar-') != -1 and not (key.find('dev') == 0):
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


if "__main__" == __name__:
    main()
