from kubernetes import client, config
from kubernetes.client import V1Container, V1PodSpec, V1ObjectMeta, V1PodTemplateSpec, V1JobTemplateSpec, V1CronJob
import yaml

class CronJobsKubernets:
    
    def __init__(self):
        # config.load_incluster_config()
        config.load_kube_config()
        self.v1 = client.BatchV1Api()

    def deleteTask(self, id, namespace, protocol):
        crons = ["http", "coap"]
        if protocol in crons:
            self.deleteCronJob(id,namespace)
        else:
            self.deleteJob(id,namespace)

    def deleteCronJob(self, id, namespace):
        try:
            api_response = self.v1.delete_namespaced_cron_job(name='cron-jobs-' + id, namespace=namespace)
            print("Cronjob eliminado exitosamente.")
        except client.rest.ApiException as e:
            print("Error al eliminar el cronjob:", e)

    def deleteJob(self, id, namespace):
        try:
            api_response = self.v1.delete_namespaced_job(name='jobs-' + id, namespace=namespace)
            print("job eliminado exitosamente.")
        except client.rest.ApiException as e:
            print("Error al eliminar el job:", e)

    def create_cronjob(self, name, namespace):
        config.load_kube_config()
        test =  {'schedule': '*/1 * * * *'}
        cron_job = V1CronJob(
            api_version="batch/v1",
            kind="CronJob",
            metadata=V1ObjectMeta(name=name, namespace=namespace),
            spec=V1JobTemplateSpec(
            **test ,
                spec=V1PodTemplateSpec(
                    spec=V1PodSpec(
                        scheduling_gates="* * * *",
                        restart_policy="OnFailure",
                        containers=[
                            V1Container(
                                name="test-cronjob-container",
                                image="busybox",
                                command=["echo", "Este es un CronJob de prueba."],
                            )

                        ],
                    )
                )
            ),
        )

        # Crea el CronJob
        try:
            self.v1.create_namespaced_cron_job(body=cron_job, namespace=namespace)
            print(f"CronJob '{name}' creado correctamente.")
        except client.rest.ApiException as e:
            print(f"Error al crear el CronJob '{name}': {e}")