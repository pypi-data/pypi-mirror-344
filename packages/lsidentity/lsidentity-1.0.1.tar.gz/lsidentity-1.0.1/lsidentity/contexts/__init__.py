import os
import uuid
from contextvars import ContextVar
from typing import Optional


def lsi_org_id_default(value: str | None = None) -> str | None:
	if value is not None:
		return value

	value = os.environ.get('LSI_ORG_ID', None)
	if value is None:
		value = os.environ.get('ORG_ID', None)
	return value


lsi_org_id_context_variable: ContextVar[Optional[str]] = ContextVar("lsi_org_id", default=None)


def lsi_account_id_default(value: str | None = None) -> str | None:
	if value is not None:
		return value

	value = os.environ.get('ACCOUNT_ID', None)
	if value is None:
		prefix = os.environ.get('APP_NAME', None)
		if prefix is not None:
			generated_id = uuid.uuid1().hex
			value = f"LSI-AID-{prefix.upper()}-{generated_id.upper()}"
	return value


lsi_account_id_context_variable: ContextVar[Optional[str]] = ContextVar("lsi_account_id", default=None)


class LsiOrgIdProvider:
	def __init__(self, org_id: str):
		self.org_id = org_id
		self.token = None

	def __enter__(self):
		self.token = lsi_org_id_context_variable.set(self.org_id)
		return self.org_id

	def __exit__(self, exc_type, exc_value, traceback):
		lsi_org_id_context_variable.reset(self.token)


class LsiOrgId:

	def __init__(self):
		pass

	def get(self):
		org_id = lsi_org_id_context_variable.get()
		return lsi_org_id_default(org_id)

	__enter__ = get

	def __exit__(self, exc_type, exc_value, traceback):
		pass


class LsiAccountIdProvider:
	def __init__(self, account_id: str):
		self.account_id = account_id
		self.token = None

	def __enter__(self):
		self.token = lsi_account_id_context_variable.set(self.account_id)
		return self.account_id

	def __exit__(self, exc_type, exc_value, traceback):
		lsi_account_id_context_variable.reset(self.token)


class LsiAccountId:

	def __init__(self):
		pass

	def get(self):
		account_id = lsi_account_id_context_variable.get()
		return lsi_account_id_default(account_id)

	__enter__ = get

	def __exit__(self, exc_type, exc_value, traceback):
		pass
