import asyncio
from typing import Any

import sentry_sdk
from celery import Celery
from celery.local import PromiseProxy

from barramento_de_mensagens.base.barramento import Evento, BarramentoDeMensagens
from barramento_de_mensagens.base.entidades import UsuarioBase

_celery_app: Celery | None = None


def configurar_celery_app(celery_app: Celery) -> None:
    global _celery_app
    _celery_app = celery_app


def obter_celery_app() -> Celery:
    if _celery_app is None:
        raise RuntimeError(
            "O celery_app ainda não foi configurado. Chame 'configurar_celery_app(celery_app)' antes de usar as tasks."
        )
    return _celery_app


def tarefa_celery(*args: dict[str, Any], **kwargs: dict[str, Any]) -> PromiseProxy:
    celery_app = obter_celery_app()

    max_retries = kwargs.pop("max_retries", 1)
    kwargs["bind"] = True
    kwargs["trail"] = True
    retry_backoff = kwargs.pop("retry_backoff", 5)
    retry_backoff_max = kwargs.pop("retry_backoff_max", 700)
    retry_jitter = kwargs.pop("retry_jitter", False)
    return celery_app.task(
        *args,
        autoretry_for=(Exception,),
        retry_kwargs={"max_retries": max_retries},
        max_retries=max_retries,
        retry_backoff=retry_backoff,
        retry_backoff_max=retry_backoff_max,
        retry_jitter=retry_jitter,
        **kwargs,
    )


@tarefa_celery()
def task_tratar_evento_asyncrono(  # type: ignore[no-untyped-def]
    self,
    evento: Evento,
    usuario: UsuarioBase | None = None,
) -> None:
    from barramento_de_mensagens.bootstrap import bootstrap_base

    async def executar(barramento: BarramentoDeMensagens, evento: Evento) -> None:
        await barramento.handle(evento)

    nome = f"Tratando evento asyncrono [{evento.__class__.__name__}]"

    contexto = sentry_sdk.start_transaction(
        name="Tratando evento asyncrono",
        op="task",
        description=nome,
        sampled=True,
    )
    with contexto as span:
        span.set_tag("name", nome)
        try:
            # A execução assíncrona começou, super importante alterar a flag do evento
            # para não ser executado de forma assíncrona novamente,
            # caso contrário o celery entrará num loop infinito de tasks
            evento.executar_de_forma_assincrona = False

            bus = bootstrap_base(usuario=usuario, subir_erros_de_eventos=True)

            # isso deve rodar dentro do asyncio.run devido a estrutura de funcoes async
            asyncio.run(executar(bus, evento))

        except Exception as erro:
            span.set_tag("houve_erro", True)
            span.set_tag("error", str(erro))
            raise erro
