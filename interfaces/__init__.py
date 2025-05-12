# Este arquivo pode estar vazio, mas vamos adicionar algumas importações úteis
from interfaces.icontroller import IController
from interfaces.imodel import IModel
from interfaces.iview import IView
from interfaces.ieventlistener import IEventListener

# Isso permite importar diretamente do pacote interfaces
__all__ = ['IController', 'IModel', 'IView', 'IEventListener']