# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2025-04-12 15:55
# @Author : 毛鹏
import os
import traceback

from playwright._impl._errors import TargetClosedError, Error, TimeoutError

from mangokit.decorator import sync_retry
from mangokit.enums import StatusEnum, ElementOperationEnum, DriveTypeEnum
from mangokit.exceptions import MangoKitError, ERROR_MSG_0015, ERROR_MSG_0010, ERROR_MSG_0048, ERROR_MSG_0054, \
    ERROR_MSG_0027, ERROR_MSG_0053, ERROR_MSG_0038, ERROR_MSG_0036
from mangokit.models import ElementResultModel, ElementModel
from mangokit.uidrive.android import AndroidDriver
from mangokit.uidrive.web.sync_web import SyncWebDevice, SyncWebAssertion


class SyncElement(SyncWebDevice, AndroidDriver):

    def __init__(self, base_data, element_model: ElementModel, drive_type: int, element_data: dict | None = None):
        super().__init__(base_data)
        self.element_data = element_data
        self.element_model = element_model
        self.drive_type = drive_type
        self.ope_name = element_model.name if element_model.name else element_model.ope_key
        self.element_test_result = ElementResultModel(
            id=self.element_model.id,
            name=self.element_model.name,
            loc=self.element_model.loc,
            exp=self.element_model.exp,
            sub=self.element_model.sub,
            sleep=self.element_model.sleep,

            type=self.element_model.type,
            ope_key=self.element_model.ope_key,
            sql=self.element_model.sql,
            key_list=self.element_model.key_list,
            key=self.element_model.key,
            value=self.element_model.value,

            status=StatusEnum.FAIL.value,
        )

    def open_device(self):
        if self.drive_type == DriveTypeEnum.WEB.value:
            self.open_url()
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.open_app()
        elif self.drive_type == DriveTypeEnum.DESKTOP.value:
            pass
        else:
            self.base_data.log(f'不存在这个类型，如果是非管理员看到这种提示，请联系管理员')
            raise Exception('不存在的设备类型')

    @sync_retry(10, 0.2)
    def element_main(self) -> ElementResultModel:
        try:
            for field_name, field_value in self.element_model:
                if field_value is None:
                    continue
                if field_name == "ope_value":
                    for method_model in field_value:
                        for method_field, method_val in method_model:
                            if isinstance(method_val, str):
                                setattr(method_model, method_field, self.base_data.test_data.replace(method_val))
                elif isinstance(field_value, str):
                    setattr(self.element_model, field_name, self.base_data.test_data.replace(field_value))
        except MangoKitError as error:
            raise MangoKitError(error.code, error.msg)

        try:
            if self.element_model.type == ElementOperationEnum.OPE.value:
                self.__ope()
            elif self.element_model.type == ElementOperationEnum.ASS.value:
                self.__ass()
            elif self.element_model.type == ElementOperationEnum.SQL.value:
                self.__sql()
            elif self.element_model.type == ElementOperationEnum.CUSTOM.value:
                self.__custom()
            else:
                raise MangoKitError(*ERROR_MSG_0015)
            if self.element_model.sleep:
                self.w_wait_for_timeout(self.element_model.sleep)
            self.element_test_result.status = StatusEnum.SUCCESS.value
            return self.element_test_result
        except TargetClosedError as error:
            self.base_data.setup()
            self.base_data.log.error(
                f'浏览器对象关闭异常，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
            self.element_test_result.status = StatusEnum.FAIL.value
            self.element_test_result.error_message = '浏览器对象被关闭，请不要认关闭浏览器，非认为管理请联系管理员解决！'
            raise MangoKitError(*ERROR_MSG_0010)
        except MangoKitError as error:
            self.__error(error)
            raise error
        except Error as error:
            self.base_data.log.error(
                f'未知错误捕获-1，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
            self.element_test_result.status = StatusEnum.FAIL.value
            self.element_test_result.error_message = f'未知错误捕获，请检查元素，如果需要明确的提示请联系管理员'
            raise error
        except Exception as error:
            self.base_data.log.error(
                f'未知错误捕获-2，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
            self.element_test_result.status = StatusEnum.FAIL.value
            self.element_test_result.error_message = f'未知错误捕获，请检查元素，如果需要明确的提示请联系管理员'
            raise error

    def __ope(self):
        method_name = getattr(self.element_model, 'ope_key', None)
        if not method_name:
            self.base_data.log.debug('操作失败-1，ope_key 不存在或为空')
            raise MangoKitError(*ERROR_MSG_0048)
        if not hasattr(self, method_name):
            self.base_data.log.debug(f'操作失败-2，方法不存在: {method_name}')
            raise MangoKitError(*ERROR_MSG_0048)
        if not callable(getattr(self, method_name)):
            self.base_data.log.debug(f'操作失败-3，属性不可调用: {method_name}')
            raise MangoKitError(*ERROR_MSG_0048)
        if self.element_model.ope_value is None:
            raise MangoKitError(*ERROR_MSG_0054)

        self.__ope_value()
        if self.drive_type == DriveTypeEnum.WEB.value:
            self.web_action_element(
                self.element_model.name,
                self.element_model.ope_key,
                {i.f: i.v for i in self.element_model.ope_value}
            )
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.a_action_element(
                self.element_model.name,
                self.element_model.ope_key,
                {i.f: i.v for i in self.element_model.ope_value}
            )
        else:
            pass
        for i in self.element_model.ope_value:
            if i.d:
                self.element_test_result.ope_value[i.p] = i.v

    def __ass(self):
        if self.element_model.ope_value is None:
            raise MangoKitError(*ERROR_MSG_0053)
        self.__ope_value(True)
        try:
            if self.drive_type == DriveTypeEnum.WEB.value:
                self.web_assertion_element(
                    self.element_model.name,
                    self.element_model.ope_key,
                    {i.f: i.v for i in self.element_model.ope_value}
                )
            elif self.drive_type == DriveTypeEnum.ANDROID.value:
                self.a_assertion_element(
                    self.element_model.name,
                    self.element_model.ope_key,
                    {i.f: i.v for i in self.element_model.ope_value}
                )
            else:
                pass
        except MangoKitError as error:
            self.element_test_result.status = StatusEnum.FAIL.value
            self.element_test_result.error_message = error.msg
            self.__error(error)
        for i in self.element_model.ope_value:
            if i.d:
                self.element_test_result.ope_value[i.p] = i.v

    def __sql(self):
        if not self.element_data:
            sql = self.base_data.test_data.replace(self.element_model.sql)
            key_list = self.element_model.key_list
        else:
            sql = self.base_data.test_data.replace(self.element_data.get('sql'))
            key_list = self.element_data.get('key_list')
        if self.base_data.mysql_connect:
            result_list: list[dict] = self.base_data.mysql_connect.condition_execute(sql)
            if isinstance(result_list, list):
                for result in result_list:
                    try:
                        for value, key in zip(result, key_list):
                            self.base_data.test_data.set_cache(key, result.get(value))
                    except SyntaxError as error:
                        self.base_data.log.debug(
                            f'SQL执行失败-1，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
                        raise MangoKitError(*ERROR_MSG_0038)

                if not result_list:
                    raise MangoKitError(*ERROR_MSG_0036, value=(self.element_model.sql,))

    def __custom(self):
        if not self.element_data:
            key = self.element_model.key
            value = self.element_model.value
        else:
            key = self.element_data.get('key')
            value = self.element_data.get('value')
        self.base_data.test_data.set_cache(key, self.base_data.test_data.replace(value))

    def __ope_value(self, is_ass: bool = False):
        try:
            ope_key = 'actual' if is_ass else 'locating'
            for i in self.element_model.ope_value:
                if i.f == ope_key and self.element_model.loc:
                    count, loc = self.__element_preset_processing()
                    if is_ass:
                        from mangokit.assertion import PublicAssertion
                        if callable(getattr(SyncWebAssertion, self.element_model.ope_key, None)):
                            i.v = loc
                        elif callable(getattr(PublicAssertion, self.element_model.ope_key, None)):
                            i.v = self.element_test_result.element_text
                    else:
                        i.v = loc
                else:
                    if self.element_data:
                        for ele_name, case_data in self.element_data.items():
                            if ele_name == i.f:
                                value = case_data
                                i.v = self.base_data.test_data.replace(value)

        except AttributeError as error:
            self.base_data.log.debug(
                f'获取操作值失败-1，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
            raise MangoKitError(*ERROR_MSG_0027)

    def __element_preset_processing(self):
        count, loc = 0, None
        find_params = {
            'name': self.element_model.name,
            '_type': self.element_model.type,
            'exp': self.element_model.exp,
            'loc': self.element_model.loc,
            'sub': self.element_model.sub
        }
        if self.drive_type == DriveTypeEnum.WEB.value:
            count, loc = self.web_find_ele(**find_params, is_iframe=self.element_model.is_iframe)
            get_text_method = self.w_get_text
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            count, loc = self.a_find_ele(**find_params)
            get_text_method = self.a_get_text
        else:
            return count, loc
        if loc is not None:
            try:
                self.element_test_result.element_text = get_text_method(loc)
            except Exception as e:
                self.base_data.log.debug(f"获取元素文本失败: {str(e)}")
        return count, loc

    def __error(self, error: MangoKitError):
        self.element_test_result.status = StatusEnum.FAIL.value
        self.element_test_result.error_message = error.msg
        self.base_data.log.debug(
            f"""
            元素操作失败----->
            元 素 对 象：{self.element_model.model_dump() if self.element_model else self.element_model}
            元素测试结果：{
            self.element_test_result.model_dump() if self.element_test_result else self.element_test_result}
            报 错 信 息：{error.msg}
            """
        )
        if self.element_test_result:
            file_name = f'失败截图-{self.element_model.name}{self.base_data.test_data.get_time_for_min()}.jpg'
            file_path = os.path.join(self.base_data.screenshot_path, file_name)
            self.element_test_result.picture_path = file_path
            self.element_test_result.picture_name = file_name
            self.__error_screenshot(file_path)

    def __error_screenshot(self, file_path):
        if self.drive_type == DriveTypeEnum.WEB.value:
            try:
                self.w_screenshot(file_path)
            except (TargetClosedError, TimeoutError) as error:
                self.base_data.log.debug(
                    f'截图出现异常失败-1，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
                self.base_data.setup()
                raise MangoKitError(*ERROR_MSG_0010)
            except AttributeError as error:
                self.base_data.log.debug(
                    f'截图出现异常失败-2，类型：{type(error)}，失败详情：{error}，失败明细：{traceback.format_exc()}')
                self.base_data.setup()
                raise MangoKitError(*ERROR_MSG_0010)
        elif self.drive_type == DriveTypeEnum.ANDROID.value:
            self.a_screenshot(file_path)
        else:
            pass
