import core
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.contrib.auth.models import AnonymousUser
from django.core import serializers
from django.forms.models import model_to_dict

from policyholder.apps import PolicyholderConfig
from policyholder.models import PolicyHolder as PolicyHolderModel, PolicyHolderUser as PolicyHolderUserModel, \
    PolicyHolderContributionPlan as PolicyHolderContributionPlanModel, PolicyHolderInsuree as PolicyHolderInsureeModel
from policyholder.validation import PolicyHolderValidation


def check_authentication(function):
    def wrapper(self, *args, **kwargs):
        if type(self.user) is AnonymousUser or not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
            }
        else:
            result = function(self, *args, **kwargs)
            return result

    return wrapper


class PolicyHolder(object):

    def __init__(self, user):
        self.user = user

    @check_authentication
    def get_by_id(self, by_policy_holder):
        try:
            ph = PolicyHolderModel.objects.get(id=by_policy_holder.id)
            uuid_string = str(ph.id)
            dict_representation = model_to_dict(ph)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolder", method="get", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def create(self, policy_holder):
        try:
            PolicyHolderValidation.validate_create(self.user, **policy_holder)
            phm = PolicyHolderModel(**policy_holder)
            phm.save(username=self.user.username)
            uuid_string = str(phm.id)
            dict_representation = model_to_dict(phm)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolder", method="create", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @staticmethod
    def check_unique_code_policy_holder(code):
        if PolicyHolderModel.objects.filter(code=code, is_deleted=False).exists():
            return [{"message": "Policy holder code %s already exists" % code}]
        return []

    @check_authentication
    def update(self, policy_holder):
        try:
            PolicyHolderValidation.validate_update(self.user, **policy_holder)
            updated_phm = PolicyHolderModel.objects.filter(id=policy_holder['id']).first()
            [setattr(updated_phm, key, policy_holder[key]) for key in policy_holder]
            updated_phm.save(username=self.user.username)
            uuid_string = str(updated_phm.id)
            dict_representation = model_to_dict(updated_phm)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolder", method="update", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def delete(self, policy_holder):
        try:
            phm_to_delete = PolicyHolderModel.objects.filter(id=policy_holder['id']).first()
            phm_to_delete.delete(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": "",
            }
        except Exception as exc:
            return _output_exception(model_name="PolicyHolder", method="delete", exception=exc)


class PolicyHolderInsuree(object):

    def __init__(self, user):
        self.user = user

    @check_authentication
    def get_by_id(self, by_policy_holder_insuree):
        try:
            phi = PolicyHolderInsureeModel.objects.get(id=by_policy_holder_insuree.id)
            uuid_string = str(phi.id)
            dict_representation = model_to_dict(phi)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderInsuree", method="get", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def create(self, policy_holder_insuree):
        try:
            phim = PolicyHolderInsureeModel(**policy_holder_insuree)
            phim.save(username=self.user.username)
            uuid_string = str(phim.id)
            dict_representation = model_to_dict(phim)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderInsuree", method="create", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def update(self, policy_holder_insuree):
        try:
            updated_phim = PolicyHolderInsureeModel.objects.filter(id=policy_holder_insuree['id']).first()
            [setattr(updated_phim, key, policy_holder_insuree[key]) for key in policy_holder_insuree]
            updated_phim.save(username=self.user.username)
            uuid_string = str(updated_phim.id)
            dict_representation = model_to_dict(updated_phim)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderInsuree", method="update", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def delete(self, policy_holder_insuree):
        try:
            phim_to_delete = PolicyHolderInsureeModel.objects.filter(id=policy_holder_insuree['id']).first()
            phim_to_delete.delete(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": "",
            }
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderInsuree", method="delete", exception=exc)

    @check_authentication
    def replace_policy_holder_insuree(self, policy_holder_insuree):
        try:
            phim_to_replace = PolicyHolderInsureeModel.objects.filter(id=policy_holder_insuree['uuid']).first()
            phim_to_replace.replace_object(data=policy_holder_insuree, username=self.user.username)
            uuid_string = str(phim_to_replace.id)
            dict_representation = model_to_dict(phim_to_replace)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderInsuree", method="replace", exception=exc)
        return {
            "success": True,
            "message": "Ok",
            "detail": "",
            "old_object": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
            "uuid_new_object": str(phim_to_replace.replacement_uuid),
        }


class PolicyHolderContributionPlan(object):

    def __init__(self, user):
        self.user = user

    @check_authentication
    def get_by_id(self, by_policy_holder_contribution_plan):
        try:
            phcp = PolicyHolderContributionPlanModel.objects.get(id=by_policy_holder_contribution_plan.id)
            uuid_string = str(phcp.id)
            dict_representation = model_to_dict(phcp)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderContributionPlan", method="get", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def create(self, policy_holder_contribution_plan):
        try:
            phcp = PolicyHolderContributionPlanModel(**policy_holder_contribution_plan)
            phcp.save(username=self.user.username)
            uuid_string = str(phcp.id)
            dict_representation = model_to_dict(phcp)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderContributionPlan", method="create", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def update(self, policy_holder_contribution_plan):
        try:
            updated_phcp = PolicyHolderContributionPlanModel.objects.filter(
                id=policy_holder_contribution_plan['id']).first()
            [setattr(updated_phcp, key, policy_holder_contribution_plan[key]) for key in
             policy_holder_contribution_plan]
            updated_phcp.save(username=self.user.username)
            uuid_string = str(updated_phcp.id)
            dict_representation = model_to_dict(updated_phcp)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderContributionPlan", method="update", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def delete(self, policy_holder_contribution_plan):
        try:
            phcp_to_delete = PolicyHolderContributionPlanModel.objects.filter(
                id=policy_holder_contribution_plan['id']).first()
            phcp_to_delete.delete(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": "",
            }
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderContributionPlan", method="delete", exception=exc)

    @check_authentication
    def replace_policy_holder_contribution_plan_bundle(self, policy_holder_contribution_plan):
        try:
            phcp_to_replace = PolicyHolderContributionPlanModel.objects.filter(
                id=policy_holder_contribution_plan['uuid']).first()
            phcp_to_replace.replace_object(data=policy_holder_contribution_plan, username=self.user.username)
            uuid_string = str(phcp_to_replace.id)
            dict_representation = model_to_dict(phcp_to_replace)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderContributionPlan", method="replace", exception=exc)
        return {
            "success": True,
            "message": "Ok",
            "detail": "",
            "old_object": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
            "uuid_new_object": str(phcp_to_replace.replacement_uuid),
        }


class PolicyHolderUser(object):

    def __init__(self, user):
        self.user = user

    @check_authentication
    def get_by_id(self, by_policy_holder_user):
        try:
            phu = PolicyHolderUserModel.objects.get(id=by_policy_holder_user.id)
            uuid_string = str(phu.id)
            dict_representation = model_to_dict(phu)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderUser", method="get", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def create(self, policy_holder_user):
        try:
            phu = PolicyHolderUserModel(**policy_holder_user)
            phu.save(username=self.user.username)
            uuid_string = str(phu.id)
            dict_representation = model_to_dict(phu)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderUser", method="create", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def update(self, policy_holder_user):
        try:
            updated_phu = PolicyHolderUserModel.objects.filter(id=policy_holder_user['id']).first()
            [setattr(updated_phu, key, policy_holder_user[key]) for key in policy_holder_user]
            updated_phu.save(username=self.user.username)
            uuid_string = str(updated_phu.id)
            dict_representation = model_to_dict(updated_phu)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderUser", method="update", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def delete(self, policy_holder_user):
        try:
            phu_to_delete = PolicyHolderUserModel.objects.filter(id=policy_holder_user['id']).first()
            phu_to_delete.delete(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": "",
            }
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderUser", method="delete", exception=exc)

    @check_authentication
    def replace_policy_holder_user(self, policy_holder_user):
        try:
            phu_to_replace = PolicyHolderUserModel.objects.filter(id=policy_holder_user['uuid']).first()
            phu_to_replace.replace_object(data=policy_holder_user, username=self.user.username)
            uuid_string = str(phu_to_replace.id)
            dict_representation = model_to_dict(phu_to_replace)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="PolicyHolderUser", method="replace", exception=exc)
        return {
            "success": True,
            "message": "Ok",
            "detail": "",
            "old_object": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
            "uuid_new_object": str(phu_to_replace.replacement_uuid),
        }


class PolicyHolderActivity(object):
    def __init__(self, user):
        self.user = user

    @check_authentication
    def get_all(self):
        return _output_result_success(PolicyholderConfig.policyholder_activity)


class PolicyHolderLegalForm(object):
    def __init__(self, user):
        self.user = user

    @check_authentication
    def get_all(self):
        return _output_result_success(PolicyholderConfig.policyholder_legal_form)


def _output_exception(model_name, method, exception):
    return {
        "success": False,
        "message": f"Failed to {method} {model_name}",
        "detail": str(exception),
        "data": "",
    }


def _output_result_success(dict_representation):
    return {
        "success": True,
        "message": "Ok",
        "detail": "",
        "data": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
    }
