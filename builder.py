import docker
import json
import click
import requests
import random

client = docker.DockerClient(base_url='tcp://127.0.0.1:2376')

@click.group()
def cli():
    pass

@cli.command('build')
@click.option("-p","--path", default="./", help="Path to your Dockerfile")
@click.option("-t","--tag", default="alpine-hello-world:latest", help="A tag to add to the final image")

def build(path, tag):
    """Bulding a container image."""
    print ("*** BUILDING IS INITIATED")
    try:
        response = client.images.build(path = path, tag=tag, rm=True)
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        click.echo(message)
    print("*** BUILD OUTPUT:")
    for object in response[1]:
          click.echo(object)
    click.echo('*** BUILDING FINISHED')

@cli.command('deploy')
@click.option("-t","--tag", default="alpine-hello-world:latest", help="The tag of the image that you want to use")
@click.option("-n","--num", default=1, help="A number of containers to deploy")
@click.argument("names", nargs=-1)
def deploy(tag,num, names):
    """Deploy a number of containers."""
    len=0
    click.echo('*** DEPLOYMENT IS INITIATED\n')
    for name in names:
       len+=1
    if (num==len):
        for name in names:
            try:
                response_container = client.containers.run(tag, name=name, detach=True)
                container_id = response_container.id
                index = slice(12)
                click.echo("Container "+container_id[index]+" was created")
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                click.echo(message)
    elif(len==1):
        for x in range(num):
            try:
                response_container = client.containers.run(tag, name=name+"_"+str(random.randrange(0,1000)), detach=True)
                container_id = response_container.id
                index = slice(12)
                click.echo("Container "+container_id[index]+" was created")
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                click.echo(message)
    else:
        click.echo("\n You have to give the same nummber of containers for generation and names OR a number of containers and one name")




@cli.command('validate')
@click.argument('containerids', nargs=-1)
def validate(containerids):
    """Validate the operation of each container."""
    flag=1
    click.echo('*** VALIDATION IS INITIATED')
    for x in containerids:
        try:
            container = client.containers.get(str(x))
            index = slice(12)
            click.echo("\nContainer(%s) has Status: %s" % (x[index], str(container.status)))
            for line in container.logs(stream=True):
                service_status_response = str(line.strip())
                if(service_status_response.find("400")<0 and str(container.status)!='exited' and str(container.status)!='paused' and str(container.status)!='dead'):
                    click.echo("Web Service(%s) has Status: running" % x[index])
                    flag=0
                    break
                else:
                    click.echo("Web Service(%s) has Status: not running" % str(x))
                    break
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            click.echo(message)


@cli.command('stats')
@click.argument('containerids', nargs=-1)
@click.option("-s", '--stream', default=0, help="Choose whether to stream (1) or not (0) the stats")
def stats(containerids, stream):
    """Monitor the resource usage of each container."""
    click.echo('*** MONITORING IS INITIATED')
    if(stream):
        while True:
            for x in containerids:
                index = slice(12)
                monitoring(containerid=x[index])
    else:
        for x in containerids:
            index = slice(12)
            monitoring(containerid=x[index])

def monitoring(containerid):
    click.echo("Container:"+containerid)
    base = "http://127.0.0.1:2376"
    url = "/containers/%s/stats?stream=0" % (containerid)
    try:
        resp = requests.get( base + url, stream=False)
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        click.echo(message)

    if resp.encoding is None:
         resp.encoding = 'utf-8'
    for line in resp.iter_lines(decode_unicode=True):
        if line:
            click.echo(json.loads(line))

@cli.command('logging')
@click.argument('filename', nargs=1, type=click.Path())
@click.argument('containerids', nargs=-1)
def logging(containerids,filename):
    """Consolidate logs of given containers into a local file."""
    click.echo('*** LOGS CONSOLIDATION IS INITIATED')
    for x in containerids:
        click.echo("Got Logs for Container:"+str(x))
        base = "http://127.0.0.1:2376"
        url = "/containers/%s/logs?stderr=1&stdout=1&tail=100&stream=0" % (str(x))
        try:
            resp = requests.get( base + url)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            click.echo(message)
        with click.open_file(filename, 'a+') as f:
            f.write("\nContainerID(%s): \n" %x)
            for line in resp:
                f.write(str(line)+"\n")


if __name__ == '__main__':
    cli()
