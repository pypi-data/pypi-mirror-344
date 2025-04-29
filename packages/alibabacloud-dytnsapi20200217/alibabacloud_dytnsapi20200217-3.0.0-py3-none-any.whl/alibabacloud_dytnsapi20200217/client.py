# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_dytnsapi20200217 import models as dytnsapi_20200217_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'central'
        self.check_config(config)
        self._endpoint = self.get_endpoint('dytnsapi', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def cert_no_three_element_verification_with_options(
        self,
        request: dytnsapi_20200217_models.CertNoThreeElementVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CertNoThreeElementVerificationResponse:
        """
        @summary 身份证三要素
        
        @param request: CertNoThreeElementVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CertNoThreeElementVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.cert_name):
            query['CertName'] = request.cert_name
        if not UtilClient.is_unset(request.cert_no):
            query['CertNo'] = request.cert_no
        if not UtilClient.is_unset(request.cert_picture):
            query['CertPicture'] = request.cert_picture
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CertNoThreeElementVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CertNoThreeElementVerificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def cert_no_three_element_verification_with_options_async(
        self,
        request: dytnsapi_20200217_models.CertNoThreeElementVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CertNoThreeElementVerificationResponse:
        """
        @summary 身份证三要素
        
        @param request: CertNoThreeElementVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CertNoThreeElementVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.cert_name):
            query['CertName'] = request.cert_name
        if not UtilClient.is_unset(request.cert_no):
            query['CertNo'] = request.cert_no
        if not UtilClient.is_unset(request.cert_picture):
            query['CertPicture'] = request.cert_picture
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CertNoThreeElementVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CertNoThreeElementVerificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def cert_no_three_element_verification(
        self,
        request: dytnsapi_20200217_models.CertNoThreeElementVerificationRequest,
    ) -> dytnsapi_20200217_models.CertNoThreeElementVerificationResponse:
        """
        @summary 身份证三要素
        
        @param request: CertNoThreeElementVerificationRequest
        @return: CertNoThreeElementVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.cert_no_three_element_verification_with_options(request, runtime)

    async def cert_no_three_element_verification_async(
        self,
        request: dytnsapi_20200217_models.CertNoThreeElementVerificationRequest,
    ) -> dytnsapi_20200217_models.CertNoThreeElementVerificationResponse:
        """
        @summary 身份证三要素
        
        @param request: CertNoThreeElementVerificationRequest
        @return: CertNoThreeElementVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.cert_no_three_element_verification_with_options_async(request, runtime)

    def cert_no_two_element_verification_with_options(
        self,
        request: dytnsapi_20200217_models.CertNoTwoElementVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CertNoTwoElementVerificationResponse:
        """
        @summary 身份证二要素认证
        
        @param request: CertNoTwoElementVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CertNoTwoElementVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.cert_name):
            query['CertName'] = request.cert_name
        if not UtilClient.is_unset(request.cert_no):
            query['CertNo'] = request.cert_no
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CertNoTwoElementVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CertNoTwoElementVerificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def cert_no_two_element_verification_with_options_async(
        self,
        request: dytnsapi_20200217_models.CertNoTwoElementVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CertNoTwoElementVerificationResponse:
        """
        @summary 身份证二要素认证
        
        @param request: CertNoTwoElementVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CertNoTwoElementVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.cert_name):
            query['CertName'] = request.cert_name
        if not UtilClient.is_unset(request.cert_no):
            query['CertNo'] = request.cert_no
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CertNoTwoElementVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CertNoTwoElementVerificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def cert_no_two_element_verification(
        self,
        request: dytnsapi_20200217_models.CertNoTwoElementVerificationRequest,
    ) -> dytnsapi_20200217_models.CertNoTwoElementVerificationResponse:
        """
        @summary 身份证二要素认证
        
        @param request: CertNoTwoElementVerificationRequest
        @return: CertNoTwoElementVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.cert_no_two_element_verification_with_options(request, runtime)

    async def cert_no_two_element_verification_async(
        self,
        request: dytnsapi_20200217_models.CertNoTwoElementVerificationRequest,
    ) -> dytnsapi_20200217_models.CertNoTwoElementVerificationResponse:
        """
        @summary 身份证二要素认证
        
        @param request: CertNoTwoElementVerificationRequest
        @return: CertNoTwoElementVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.cert_no_two_element_verification_with_options_async(request, runtime)

    def company_four_elements_verification_with_options(
        self,
        request: dytnsapi_20200217_models.CompanyFourElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CompanyFourElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name, the business license number, and the name and ID card of the legal representative belong to the same enterprise. The verification is successful only when the preceding four elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to four-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0, 1, or 2.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyFourElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CompanyFourElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.ep_cert_name):
            query['EpCertName'] = request.ep_cert_name
        if not UtilClient.is_unset(request.ep_cert_no):
            query['EpCertNo'] = request.ep_cert_no
        if not UtilClient.is_unset(request.legal_person_cert_name):
            query['LegalPersonCertName'] = request.legal_person_cert_name
        if not UtilClient.is_unset(request.legal_person_cert_no):
            query['LegalPersonCertNo'] = request.legal_person_cert_no
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CompanyFourElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CompanyFourElementsVerificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def company_four_elements_verification_with_options_async(
        self,
        request: dytnsapi_20200217_models.CompanyFourElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CompanyFourElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name, the business license number, and the name and ID card of the legal representative belong to the same enterprise. The verification is successful only when the preceding four elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to four-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0, 1, or 2.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyFourElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CompanyFourElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.ep_cert_name):
            query['EpCertName'] = request.ep_cert_name
        if not UtilClient.is_unset(request.ep_cert_no):
            query['EpCertNo'] = request.ep_cert_no
        if not UtilClient.is_unset(request.legal_person_cert_name):
            query['LegalPersonCertName'] = request.legal_person_cert_name
        if not UtilClient.is_unset(request.legal_person_cert_no):
            query['LegalPersonCertNo'] = request.legal_person_cert_no
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CompanyFourElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CompanyFourElementsVerificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def company_four_elements_verification(
        self,
        request: dytnsapi_20200217_models.CompanyFourElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.CompanyFourElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name, the business license number, and the name and ID card of the legal representative belong to the same enterprise. The verification is successful only when the preceding four elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to four-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0, 1, or 2.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyFourElementsVerificationRequest
        @return: CompanyFourElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.company_four_elements_verification_with_options(request, runtime)

    async def company_four_elements_verification_async(
        self,
        request: dytnsapi_20200217_models.CompanyFourElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.CompanyFourElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name, the business license number, and the name and ID card of the legal representative belong to the same enterprise. The verification is successful only when the preceding four elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to four-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0, 1, or 2.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyFourElementsVerificationRequest
        @return: CompanyFourElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.company_four_elements_verification_with_options_async(request, runtime)

    def company_three_elements_verification_with_options(
        self,
        request: dytnsapi_20200217_models.CompanyThreeElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CompanyThreeElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name, the business license number, and the name of the legal representative belong to the same enterprise. The verification is successful only when the three elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to three-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0, 1, or 2.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyThreeElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CompanyThreeElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.ep_cert_name):
            query['EpCertName'] = request.ep_cert_name
        if not UtilClient.is_unset(request.ep_cert_no):
            query['EpCertNo'] = request.ep_cert_no
        if not UtilClient.is_unset(request.legal_person_cert_name):
            query['LegalPersonCertName'] = request.legal_person_cert_name
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CompanyThreeElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CompanyThreeElementsVerificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def company_three_elements_verification_with_options_async(
        self,
        request: dytnsapi_20200217_models.CompanyThreeElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CompanyThreeElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name, the business license number, and the name of the legal representative belong to the same enterprise. The verification is successful only when the three elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to three-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0, 1, or 2.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyThreeElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CompanyThreeElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.ep_cert_name):
            query['EpCertName'] = request.ep_cert_name
        if not UtilClient.is_unset(request.ep_cert_no):
            query['EpCertNo'] = request.ep_cert_no
        if not UtilClient.is_unset(request.legal_person_cert_name):
            query['LegalPersonCertName'] = request.legal_person_cert_name
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CompanyThreeElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CompanyThreeElementsVerificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def company_three_elements_verification(
        self,
        request: dytnsapi_20200217_models.CompanyThreeElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.CompanyThreeElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name, the business license number, and the name of the legal representative belong to the same enterprise. The verification is successful only when the three elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to three-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0, 1, or 2.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyThreeElementsVerificationRequest
        @return: CompanyThreeElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.company_three_elements_verification_with_options(request, runtime)

    async def company_three_elements_verification_async(
        self,
        request: dytnsapi_20200217_models.CompanyThreeElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.CompanyThreeElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name, the business license number, and the name of the legal representative belong to the same enterprise. The verification is successful only when the three elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to three-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0, 1, or 2.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyThreeElementsVerificationRequest
        @return: CompanyThreeElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.company_three_elements_verification_with_options_async(request, runtime)

    def company_two_elements_verification_with_options(
        self,
        request: dytnsapi_20200217_models.CompanyTwoElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CompanyTwoElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name and the business license number belong to the same enterprise. The verification is successful only when the two elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to two-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0 or 1.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyTwoElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CompanyTwoElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.ep_cert_name):
            query['EpCertName'] = request.ep_cert_name
        if not UtilClient.is_unset(request.ep_cert_no):
            query['EpCertNo'] = request.ep_cert_no
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CompanyTwoElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CompanyTwoElementsVerificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def company_two_elements_verification_with_options_async(
        self,
        request: dytnsapi_20200217_models.CompanyTwoElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.CompanyTwoElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name and the business license number belong to the same enterprise. The verification is successful only when the two elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to two-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0 or 1.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyTwoElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CompanyTwoElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.ep_cert_name):
            query['EpCertName'] = request.ep_cert_name
        if not UtilClient.is_unset(request.ep_cert_no):
            query['EpCertNo'] = request.ep_cert_no
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CompanyTwoElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.CompanyTwoElementsVerificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def company_two_elements_verification(
        self,
        request: dytnsapi_20200217_models.CompanyTwoElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.CompanyTwoElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name and the business license number belong to the same enterprise. The verification is successful only when the two elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to two-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0 or 1.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyTwoElementsVerificationRequest
        @return: CompanyTwoElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.company_two_elements_verification_with_options(request, runtime)

    async def company_two_elements_verification_async(
        self,
        request: dytnsapi_20200217_models.CompanyTwoElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.CompanyTwoElementsVerificationResponse:
        """
        @summary Verifies whether the enterprise name and the business license number belong to the same enterprise. The verification is successful only when the two elements belong to the same enterprise and the business status of the enterprise is Active.
        
        @description    Before you call this operation, make sure that you are familiar with the billing of services related to two-element verification for enterprises. For more information, see [Billing](https://help.aliyun.com/document_detail/154751.html?spm=a2c4g.154007.0.0.3edd7eb6E90YT4).
        You are charged only if the value of VerifyResult is true or false and the value of ReasonCode is 0 or 1.
        Before you call this operation, perform the following operations: Log on to the [Cell Phone Number Service console](https://account.aliyun.com/login/login.htm?oauth_callback=https%3A%2F%2Fdytns.console.aliyun.com%2Foverview%3Fspm%3Da2c4g.608385.0.0.79847f8b3awqUC\\&lang=zh). On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: CompanyTwoElementsVerificationRequest
        @return: CompanyTwoElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.company_two_elements_verification_with_options_async(request, runtime)

    def describe_empty_number_with_options(
        self,
        request: dytnsapi_20200217_models.DescribeEmptyNumberRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribeEmptyNumberResponse:
        """
        @summary Predicts whether a phone number is a nonexistent number by using AI algorithms.
        
        @description    You can call this operation to verify whether a phone number is a nonexistent number. When you call this operation to verify a number, the system charges you CNY 0.01 per verification based on the number of verifications. **Before you call this operation, make sure that you are familiar with the billing of Cell Phone Number Service.**\
        You are charged only if the value of Code is OK and the value of Status is not UNKNOWN.
        The prediction is not strictly accurate because Cell Phone Number Service predicts the nonexistent number probability by using AI algorithms. The accuracy rate of the prediction and the recall rate of empty numbers are about 95%. **Pay attention to this point when you call this operation**.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 100 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        ### [](#)Authorization information
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        
        @param request: DescribeEmptyNumberRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeEmptyNumberResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeEmptyNumber',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribeEmptyNumberResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_empty_number_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribeEmptyNumberRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribeEmptyNumberResponse:
        """
        @summary Predicts whether a phone number is a nonexistent number by using AI algorithms.
        
        @description    You can call this operation to verify whether a phone number is a nonexistent number. When you call this operation to verify a number, the system charges you CNY 0.01 per verification based on the number of verifications. **Before you call this operation, make sure that you are familiar with the billing of Cell Phone Number Service.**\
        You are charged only if the value of Code is OK and the value of Status is not UNKNOWN.
        The prediction is not strictly accurate because Cell Phone Number Service predicts the nonexistent number probability by using AI algorithms. The accuracy rate of the prediction and the recall rate of empty numbers are about 95%. **Pay attention to this point when you call this operation**.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 100 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        ### [](#)Authorization information
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        
        @param request: DescribeEmptyNumberRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeEmptyNumberResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeEmptyNumber',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribeEmptyNumberResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_empty_number(
        self,
        request: dytnsapi_20200217_models.DescribeEmptyNumberRequest,
    ) -> dytnsapi_20200217_models.DescribeEmptyNumberResponse:
        """
        @summary Predicts whether a phone number is a nonexistent number by using AI algorithms.
        
        @description    You can call this operation to verify whether a phone number is a nonexistent number. When you call this operation to verify a number, the system charges you CNY 0.01 per verification based on the number of verifications. **Before you call this operation, make sure that you are familiar with the billing of Cell Phone Number Service.**\
        You are charged only if the value of Code is OK and the value of Status is not UNKNOWN.
        The prediction is not strictly accurate because Cell Phone Number Service predicts the nonexistent number probability by using AI algorithms. The accuracy rate of the prediction and the recall rate of empty numbers are about 95%. **Pay attention to this point when you call this operation**.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 100 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        ### [](#)Authorization information
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        
        @param request: DescribeEmptyNumberRequest
        @return: DescribeEmptyNumberResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_empty_number_with_options(request, runtime)

    async def describe_empty_number_async(
        self,
        request: dytnsapi_20200217_models.DescribeEmptyNumberRequest,
    ) -> dytnsapi_20200217_models.DescribeEmptyNumberResponse:
        """
        @summary Predicts whether a phone number is a nonexistent number by using AI algorithms.
        
        @description    You can call this operation to verify whether a phone number is a nonexistent number. When you call this operation to verify a number, the system charges you CNY 0.01 per verification based on the number of verifications. **Before you call this operation, make sure that you are familiar with the billing of Cell Phone Number Service.**\
        You are charged only if the value of Code is OK and the value of Status is not UNKNOWN.
        The prediction is not strictly accurate because Cell Phone Number Service predicts the nonexistent number probability by using AI algorithms. The accuracy rate of the prediction and the recall rate of empty numbers are about 95%. **Pay attention to this point when you call this operation**.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 100 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        ### [](#)Authorization information
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        
        @param request: DescribeEmptyNumberRequest
        @return: DescribeEmptyNumberResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_empty_number_with_options_async(request, runtime)

    def describe_mobile_operator_attribute_with_options(
        self,
        request: dytnsapi_20200217_models.DescribeMobileOperatorAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribeMobileOperatorAttributeResponse:
        """
        @summary 号码归属地查询v2
        
        @param request: DescribeMobileOperatorAttributeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeMobileOperatorAttributeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeMobileOperatorAttribute',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribeMobileOperatorAttributeResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_mobile_operator_attribute_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribeMobileOperatorAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribeMobileOperatorAttributeResponse:
        """
        @summary 号码归属地查询v2
        
        @param request: DescribeMobileOperatorAttributeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeMobileOperatorAttributeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribeMobileOperatorAttribute',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribeMobileOperatorAttributeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_mobile_operator_attribute(
        self,
        request: dytnsapi_20200217_models.DescribeMobileOperatorAttributeRequest,
    ) -> dytnsapi_20200217_models.DescribeMobileOperatorAttributeResponse:
        """
        @summary 号码归属地查询v2
        
        @param request: DescribeMobileOperatorAttributeRequest
        @return: DescribeMobileOperatorAttributeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_mobile_operator_attribute_with_options(request, runtime)

    async def describe_mobile_operator_attribute_async(
        self,
        request: dytnsapi_20200217_models.DescribeMobileOperatorAttributeRequest,
    ) -> dytnsapi_20200217_models.DescribeMobileOperatorAttributeResponse:
        """
        @summary 号码归属地查询v2
        
        @param request: DescribeMobileOperatorAttributeRequest
        @return: DescribeMobileOperatorAttributeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_mobile_operator_attribute_with_options_async(request, runtime)

    def describe_phone_number_analysis_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisResponse:
        """
        @summary 号码分析实时查询蚂蚁
        
        @param request: DescribePhoneNumberAnalysisRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAnalysisResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.number_type):
            query['NumberType'] = request.number_type
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.rate):
            query['Rate'] = request.rate
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAnalysis',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAnalysisResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_analysis_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisResponse:
        """
        @summary 号码分析实时查询蚂蚁
        
        @param request: DescribePhoneNumberAnalysisRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAnalysisResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.number_type):
            query['NumberType'] = request.number_type
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.rate):
            query['Rate'] = request.rate
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAnalysis',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAnalysisResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_analysis(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisResponse:
        """
        @summary 号码分析实时查询蚂蚁
        
        @param request: DescribePhoneNumberAnalysisRequest
        @return: DescribePhoneNumberAnalysisResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_analysis_with_options(request, runtime)

    async def describe_phone_number_analysis_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisResponse:
        """
        @summary 号码分析实时查询蚂蚁
        
        @param request: DescribePhoneNumberAnalysisRequest
        @return: DescribePhoneNumberAnalysisResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_analysis_with_options_async(request, runtime)

    def describe_phone_number_analysis_aiwith_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIResponse:
        """
        @summary Obtains the analysis results of a phone number.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the Labels page, find the label that you want to use, click Activate Now, enter the required information, and then submit your application. After your application is approved, you can use the label. Before you call this operation, make sure that you are familiar with the billing of Cell Phone Number Service.
        
        @param request: DescribePhoneNumberAnalysisAIRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAnalysisAIResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.model_config):
            query['ModelConfig'] = request.model_config
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.rate):
            query['Rate'] = request.rate
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAnalysisAI',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_analysis_aiwith_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIResponse:
        """
        @summary Obtains the analysis results of a phone number.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the Labels page, find the label that you want to use, click Activate Now, enter the required information, and then submit your application. After your application is approved, you can use the label. Before you call this operation, make sure that you are familiar with the billing of Cell Phone Number Service.
        
        @param request: DescribePhoneNumberAnalysisAIRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAnalysisAIResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.model_config):
            query['ModelConfig'] = request.model_config
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.rate):
            query['Rate'] = request.rate
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAnalysisAI',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_analysis_ai(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIResponse:
        """
        @summary Obtains the analysis results of a phone number.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the Labels page, find the label that you want to use, click Activate Now, enter the required information, and then submit your application. After your application is approved, you can use the label. Before you call this operation, make sure that you are familiar with the billing of Cell Phone Number Service.
        
        @param request: DescribePhoneNumberAnalysisAIRequest
        @return: DescribePhoneNumberAnalysisAIResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_analysis_aiwith_options(request, runtime)

    async def describe_phone_number_analysis_ai_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisAIResponse:
        """
        @summary Obtains the analysis results of a phone number.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the Labels page, find the label that you want to use, click Activate Now, enter the required information, and then submit your application. After your application is approved, you can use the label. Before you call this operation, make sure that you are familiar with the billing of Cell Phone Number Service.
        
        @param request: DescribePhoneNumberAnalysisAIRequest
        @return: DescribePhoneNumberAnalysisAIResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_analysis_aiwith_options_async(request, runtime)

    def describe_phone_number_analysis_pai_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiResponse:
        """
        @summary 号码分析服务pai供应商批量查询接口
        
        @param request: DescribePhoneNumberAnalysisPaiRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAnalysisPaiResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.model_config):
            query['ModelConfig'] = request.model_config
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.rate):
            query['Rate'] = request.rate
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAnalysisPai',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_analysis_pai_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiResponse:
        """
        @summary 号码分析服务pai供应商批量查询接口
        
        @param request: DescribePhoneNumberAnalysisPaiRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAnalysisPaiResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.model_config):
            query['ModelConfig'] = request.model_config
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.rate):
            query['Rate'] = request.rate
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAnalysisPai',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_analysis_pai(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiResponse:
        """
        @summary 号码分析服务pai供应商批量查询接口
        
        @param request: DescribePhoneNumberAnalysisPaiRequest
        @return: DescribePhoneNumberAnalysisPaiResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_analysis_pai_with_options(request, runtime)

    async def describe_phone_number_analysis_pai_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisPaiResponse:
        """
        @summary 号码分析服务pai供应商批量查询接口
        
        @param request: DescribePhoneNumberAnalysisPaiRequest
        @return: DescribePhoneNumberAnalysisPaiResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_analysis_pai_with_options_async(request, runtime)

    def describe_phone_number_analysis_transparent_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentResponse:
        """
        @summary 泛行业人群筛选
        
        @param request: DescribePhoneNumberAnalysisTransparentRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAnalysisTransparentResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.ip):
            query['Ip'] = request.ip
        if not UtilClient.is_unset(request.number_type):
            query['NumberType'] = request.number_type
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAnalysisTransparent',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_analysis_transparent_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentResponse:
        """
        @summary 泛行业人群筛选
        
        @param request: DescribePhoneNumberAnalysisTransparentRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAnalysisTransparentResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.ip):
            query['Ip'] = request.ip
        if not UtilClient.is_unset(request.number_type):
            query['NumberType'] = request.number_type
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAnalysisTransparent',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_analysis_transparent(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentResponse:
        """
        @summary 泛行业人群筛选
        
        @param request: DescribePhoneNumberAnalysisTransparentRequest
        @return: DescribePhoneNumberAnalysisTransparentResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_analysis_transparent_with_options(request, runtime)

    async def describe_phone_number_analysis_transparent_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAnalysisTransparentResponse:
        """
        @summary 泛行业人群筛选
        
        @param request: DescribePhoneNumberAnalysisTransparentRequest
        @return: DescribePhoneNumberAnalysisTransparentResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_analysis_transparent_with_options_async(request, runtime)

    def describe_phone_number_attribute_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAttributeResponse:
        """
        @deprecated OpenAPI DescribePhoneNumberAttribute is deprecated, please use Dytnsapi::2020-02-17::DescribePhoneNumberOperatorAttribute instead.
        
        @summary Queries the carrier, registration location, and mobile number portability information of a phone number.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        ### [](#qps)QPS limits
        You can call this operation up to 2,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: DescribePhoneNumberAttributeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAttributeResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.phone_number):
            query['PhoneNumber'] = request.phone_number
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAttribute',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAttributeResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_attribute_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAttributeResponse:
        """
        @deprecated OpenAPI DescribePhoneNumberAttribute is deprecated, please use Dytnsapi::2020-02-17::DescribePhoneNumberOperatorAttribute instead.
        
        @summary Queries the carrier, registration location, and mobile number portability information of a phone number.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        ### [](#qps)QPS limits
        You can call this operation up to 2,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: DescribePhoneNumberAttributeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberAttributeResponse
        Deprecated
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.phone_number):
            query['PhoneNumber'] = request.phone_number
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberAttribute',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberAttributeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_attribute(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAttributeRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAttributeResponse:
        """
        @deprecated OpenAPI DescribePhoneNumberAttribute is deprecated, please use Dytnsapi::2020-02-17::DescribePhoneNumberOperatorAttribute instead.
        
        @summary Queries the carrier, registration location, and mobile number portability information of a phone number.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        ### [](#qps)QPS limits
        You can call this operation up to 2,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: DescribePhoneNumberAttributeRequest
        @return: DescribePhoneNumberAttributeResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_attribute_with_options(request, runtime)

    async def describe_phone_number_attribute_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberAttributeRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberAttributeResponse:
        """
        @deprecated OpenAPI DescribePhoneNumberAttribute is deprecated, please use Dytnsapi::2020-02-17::DescribePhoneNumberOperatorAttribute instead.
        
        @summary Queries the carrier, registration location, and mobile number portability information of a phone number.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        ### [](#qps)QPS limits
        You can call this operation up to 2,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: DescribePhoneNumberAttributeRequest
        @return: DescribePhoneNumberAttributeResponse
        Deprecated
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_attribute_with_options_async(request, runtime)

    def describe_phone_number_online_time_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeResponse:
        """
        @summary Queries the usage period of a phone number of a user.
        
        @description    Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: DescribePhoneNumberOnlineTimeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberOnlineTimeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberOnlineTime',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_online_time_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeResponse:
        """
        @summary Queries the usage period of a phone number of a user.
        
        @description    Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: DescribePhoneNumberOnlineTimeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberOnlineTimeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberOnlineTime',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_online_time(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeResponse:
        """
        @summary Queries the usage period of a phone number of a user.
        
        @description    Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: DescribePhoneNumberOnlineTimeRequest
        @return: DescribePhoneNumberOnlineTimeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_online_time_with_options(request, runtime)

    async def describe_phone_number_online_time_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOnlineTimeResponse:
        """
        @summary Queries the usage period of a phone number of a user.
        
        @description    Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: DescribePhoneNumberOnlineTimeRequest
        @return: DescribePhoneNumberOnlineTimeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_online_time_with_options_async(request, runtime)

    def describe_phone_number_operator_attribute_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeResponse:
        """
        @summary Queries the attribute information about a phone number, including the registration province, registration city, basic carrier (such as China Mobile, China Unicom, China Telecom, or China Broadnet), reseller of mobile communications services (such as Alibaba Communications), mobile number portability, and the number segment to which the phone number belongs.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154008.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        You can call this operation to obtain the carrier, registration location, and mobile number portability information about a phone number. You can query phone numbers in **plaintext** and phone numbers that are encrypted by using **MD5** and **SHA256**.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: DescribePhoneNumberOperatorAttributeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberOperatorAttributeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.flow_name):
            query['FlowName'] = request.flow_name
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.result_count):
            query['ResultCount'] = request.result_count
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberOperatorAttribute',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_operator_attribute_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeResponse:
        """
        @summary Queries the attribute information about a phone number, including the registration province, registration city, basic carrier (such as China Mobile, China Unicom, China Telecom, or China Broadnet), reseller of mobile communications services (such as Alibaba Communications), mobile number portability, and the number segment to which the phone number belongs.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154008.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        You can call this operation to obtain the carrier, registration location, and mobile number portability information about a phone number. You can query phone numbers in **plaintext** and phone numbers that are encrypted by using **MD5** and **SHA256**.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: DescribePhoneNumberOperatorAttributeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberOperatorAttributeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.flow_name):
            query['FlowName'] = request.flow_name
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.result_count):
            query['ResultCount'] = request.result_count
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberOperatorAttribute',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_operator_attribute(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeResponse:
        """
        @summary Queries the attribute information about a phone number, including the registration province, registration city, basic carrier (such as China Mobile, China Unicom, China Telecom, or China Broadnet), reseller of mobile communications services (such as Alibaba Communications), mobile number portability, and the number segment to which the phone number belongs.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154008.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        You can call this operation to obtain the carrier, registration location, and mobile number portability information about a phone number. You can query phone numbers in **plaintext** and phone numbers that are encrypted by using **MD5** and **SHA256**.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: DescribePhoneNumberOperatorAttributeRequest
        @return: DescribePhoneNumberOperatorAttributeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_operator_attribute_with_options(request, runtime)

    async def describe_phone_number_operator_attribute_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeResponse:
        """
        @summary Queries the attribute information about a phone number, including the registration province, registration city, basic carrier (such as China Mobile, China Unicom, China Telecom, or China Broadnet), reseller of mobile communications services (such as Alibaba Communications), mobile number portability, and the number segment to which the phone number belongs.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154008.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        You can call this operation to obtain the carrier, registration location, and mobile number portability information about a phone number. You can query phone numbers in **plaintext** and phone numbers that are encrypted by using **MD5** and **SHA256**.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        
        @param request: DescribePhoneNumberOperatorAttributeRequest
        @return: DescribePhoneNumberOperatorAttributeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_operator_attribute_with_options_async(request, runtime)

    def describe_phone_number_operator_attribute_annual_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualResponse:
        """
        @summary 号码归属服务(包年包月客户专用)
        
        @param request: DescribePhoneNumberOperatorAttributeAnnualRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberOperatorAttributeAnnualResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.number):
            query['Number'] = request.number
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberOperatorAttributeAnnual',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_operator_attribute_annual_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualResponse:
        """
        @summary 号码归属服务(包年包月客户专用)
        
        @param request: DescribePhoneNumberOperatorAttributeAnnualRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberOperatorAttributeAnnualResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.number):
            query['Number'] = request.number
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberOperatorAttributeAnnual',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_operator_attribute_annual(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualResponse:
        """
        @summary 号码归属服务(包年包月客户专用)
        
        @param request: DescribePhoneNumberOperatorAttributeAnnualRequest
        @return: DescribePhoneNumberOperatorAttributeAnnualResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_operator_attribute_annual_with_options(request, runtime)

    async def describe_phone_number_operator_attribute_annual_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualResponse:
        """
        @summary 号码归属服务(包年包月客户专用)
        
        @param request: DescribePhoneNumberOperatorAttributeAnnualRequest
        @return: DescribePhoneNumberOperatorAttributeAnnualResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_operator_attribute_annual_with_options_async(request, runtime)

    def describe_phone_number_operator_attribute_annual_use_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseResponse:
        """
        @summary 号码归属服务(包年包月客户专用)
        
        @param request: DescribePhoneNumberOperatorAttributeAnnualUseRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberOperatorAttributeAnnualUseResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberOperatorAttributeAnnualUse',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_operator_attribute_annual_use_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseResponse:
        """
        @summary 号码归属服务(包年包月客户专用)
        
        @param request: DescribePhoneNumberOperatorAttributeAnnualUseRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberOperatorAttributeAnnualUseResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberOperatorAttributeAnnualUse',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_operator_attribute_annual_use(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseResponse:
        """
        @summary 号码归属服务(包年包月客户专用)
        
        @param request: DescribePhoneNumberOperatorAttributeAnnualUseRequest
        @return: DescribePhoneNumberOperatorAttributeAnnualUseResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_operator_attribute_annual_use_with_options(request, runtime)

    async def describe_phone_number_operator_attribute_annual_use_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberOperatorAttributeAnnualUseResponse:
        """
        @summary 号码归属服务(包年包月客户专用)
        
        @param request: DescribePhoneNumberOperatorAttributeAnnualUseRequest
        @return: DescribePhoneNumberOperatorAttributeAnnualUseResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_operator_attribute_annual_use_with_options_async(request, runtime)

    def describe_phone_number_risk_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberRiskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberRiskResponse:
        """
        @summary 风险用户评分
        
        @param request: DescribePhoneNumberRiskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberRiskResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberRisk',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberRiskResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_number_risk_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberRiskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberRiskResponse:
        """
        @summary 风险用户评分
        
        @param request: DescribePhoneNumberRiskRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneNumberRiskResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneNumberRisk',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneNumberRiskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_number_risk(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberRiskRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberRiskResponse:
        """
        @summary 风险用户评分
        
        @param request: DescribePhoneNumberRiskRequest
        @return: DescribePhoneNumberRiskResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_number_risk_with_options(request, runtime)

    async def describe_phone_number_risk_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneNumberRiskRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneNumberRiskResponse:
        """
        @summary 风险用户评分
        
        @param request: DescribePhoneNumberRiskRequest
        @return: DescribePhoneNumberRiskResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_number_risk_with_options_async(request, runtime)

    def describe_phone_twice_tel_verify_with_options(
        self,
        request: dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyResponse:
        """
        @summary Verifies whether a phone number is a reassigned phone number by calling this operation.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        You are charged for phone number verifications only if the value of Code is OK and the value of VerifyResult is not 0.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ## [](#qps)QPS limits
        You can call this operation up to 100 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        ## [](#)Authorization information
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        
        @param request: DescribePhoneTwiceTelVerifyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneTwiceTelVerifyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneTwiceTelVerify',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_phone_twice_tel_verify_with_options_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyResponse:
        """
        @summary Verifies whether a phone number is a reassigned phone number by calling this operation.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        You are charged for phone number verifications only if the value of Code is OK and the value of VerifyResult is not 0.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ## [](#qps)QPS limits
        You can call this operation up to 100 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        ## [](#)Authorization information
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        
        @param request: DescribePhoneTwiceTelVerifyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribePhoneTwiceTelVerifyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DescribePhoneTwiceTelVerify',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_phone_twice_tel_verify(
        self,
        request: dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyResponse:
        """
        @summary Verifies whether a phone number is a reassigned phone number by calling this operation.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        You are charged for phone number verifications only if the value of Code is OK and the value of VerifyResult is not 0.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ## [](#qps)QPS limits
        You can call this operation up to 100 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        ## [](#)Authorization information
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        
        @param request: DescribePhoneTwiceTelVerifyRequest
        @return: DescribePhoneTwiceTelVerifyResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_phone_twice_tel_verify_with_options(request, runtime)

    async def describe_phone_twice_tel_verify_async(
        self,
        request: dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyRequest,
    ) -> dytnsapi_20200217_models.DescribePhoneTwiceTelVerifyResponse:
        """
        @summary Verifies whether a phone number is a reassigned phone number by calling this operation.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        You are charged for phone number verifications only if the value of Code is OK and the value of VerifyResult is not 0.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ## [](#qps)QPS limits
        You can call this operation up to 100 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        ## [](#)Authorization information
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        
        @param request: DescribePhoneTwiceTelVerifyRequest
        @return: DescribePhoneTwiceTelVerifyResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_phone_twice_tel_verify_with_options_async(request, runtime)

    def get_uaidapply_token_sign_with_options(
        self,
        request: dytnsapi_20200217_models.GetUAIDApplyTokenSignRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.GetUAIDApplyTokenSignResponse:
        """
        @summary 获取UAID申请Token所需的签名字段
        
        @param request: GetUAIDApplyTokenSignRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUAIDApplyTokenSignResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.client_type):
            query['ClientType'] = request.client_type
        if not UtilClient.is_unset(request.format):
            query['Format'] = request.format
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.param_key):
            query['ParamKey'] = request.param_key
        if not UtilClient.is_unset(request.param_str):
            query['ParamStr'] = request.param_str
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.time):
            query['Time'] = request.time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUAIDApplyTokenSign',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.GetUAIDApplyTokenSignResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_uaidapply_token_sign_with_options_async(
        self,
        request: dytnsapi_20200217_models.GetUAIDApplyTokenSignRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.GetUAIDApplyTokenSignResponse:
        """
        @summary 获取UAID申请Token所需的签名字段
        
        @param request: GetUAIDApplyTokenSignRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUAIDApplyTokenSignResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.client_type):
            query['ClientType'] = request.client_type
        if not UtilClient.is_unset(request.format):
            query['Format'] = request.format
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.param_key):
            query['ParamKey'] = request.param_key
        if not UtilClient.is_unset(request.param_str):
            query['ParamStr'] = request.param_str
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.time):
            query['Time'] = request.time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUAIDApplyTokenSign',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.GetUAIDApplyTokenSignResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_uaidapply_token_sign(
        self,
        request: dytnsapi_20200217_models.GetUAIDApplyTokenSignRequest,
    ) -> dytnsapi_20200217_models.GetUAIDApplyTokenSignResponse:
        """
        @summary 获取UAID申请Token所需的签名字段
        
        @param request: GetUAIDApplyTokenSignRequest
        @return: GetUAIDApplyTokenSignResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_uaidapply_token_sign_with_options(request, runtime)

    async def get_uaidapply_token_sign_async(
        self,
        request: dytnsapi_20200217_models.GetUAIDApplyTokenSignRequest,
    ) -> dytnsapi_20200217_models.GetUAIDApplyTokenSignResponse:
        """
        @summary 获取UAID申请Token所需的签名字段
        
        @param request: GetUAIDApplyTokenSignRequest
        @return: GetUAIDApplyTokenSignResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_uaidapply_token_sign_with_options_async(request, runtime)

    def get_uaidconversion_sign_with_options(
        self,
        request: dytnsapi_20200217_models.GetUAIDConversionSignRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.GetUAIDConversionSignResponse:
        """
        @summary 获取号码采集服务申请Token所需的签名字段
        
        @param request: GetUAIDConversionSignRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUAIDConversionSignResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.client_type):
            query['ClientType'] = request.client_type
        if not UtilClient.is_unset(request.format):
            query['Format'] = request.format
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.param_key):
            query['ParamKey'] = request.param_key
        if not UtilClient.is_unset(request.param_str):
            query['ParamStr'] = request.param_str
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.time):
            query['Time'] = request.time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUAIDConversionSign',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.GetUAIDConversionSignResponse(),
            self.call_api(params, req, runtime)
        )

    async def get_uaidconversion_sign_with_options_async(
        self,
        request: dytnsapi_20200217_models.GetUAIDConversionSignRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.GetUAIDConversionSignResponse:
        """
        @summary 获取号码采集服务申请Token所需的签名字段
        
        @param request: GetUAIDConversionSignRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GetUAIDConversionSignResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.client_type):
            query['ClientType'] = request.client_type
        if not UtilClient.is_unset(request.format):
            query['Format'] = request.format
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.param_key):
            query['ParamKey'] = request.param_key
        if not UtilClient.is_unset(request.param_str):
            query['ParamStr'] = request.param_str
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.time):
            query['Time'] = request.time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUAIDConversionSign',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.GetUAIDConversionSignResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def get_uaidconversion_sign(
        self,
        request: dytnsapi_20200217_models.GetUAIDConversionSignRequest,
    ) -> dytnsapi_20200217_models.GetUAIDConversionSignResponse:
        """
        @summary 获取号码采集服务申请Token所需的签名字段
        
        @param request: GetUAIDConversionSignRequest
        @return: GetUAIDConversionSignResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.get_uaidconversion_sign_with_options(request, runtime)

    async def get_uaidconversion_sign_async(
        self,
        request: dytnsapi_20200217_models.GetUAIDConversionSignRequest,
    ) -> dytnsapi_20200217_models.GetUAIDConversionSignResponse:
        """
        @summary 获取号码采集服务申请Token所需的签名字段
        
        @param request: GetUAIDConversionSignRequest
        @return: GetUAIDConversionSignResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.get_uaidconversion_sign_with_options_async(request, runtime)

    def invalid_phone_number_filter_with_options(
        self,
        request: dytnsapi_20200217_models.InvalidPhoneNumberFilterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.InvalidPhoneNumberFilterResponse:
        """
        @summary Filters invalid phone numbers.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click *Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 1,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: InvalidPhoneNumberFilterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvalidPhoneNumberFilterResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InvalidPhoneNumberFilter',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.InvalidPhoneNumberFilterResponse(),
            self.call_api(params, req, runtime)
        )

    async def invalid_phone_number_filter_with_options_async(
        self,
        request: dytnsapi_20200217_models.InvalidPhoneNumberFilterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.InvalidPhoneNumberFilterResponse:
        """
        @summary Filters invalid phone numbers.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click *Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 1,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: InvalidPhoneNumberFilterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvalidPhoneNumberFilterResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InvalidPhoneNumberFilter',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.InvalidPhoneNumberFilterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def invalid_phone_number_filter(
        self,
        request: dytnsapi_20200217_models.InvalidPhoneNumberFilterRequest,
    ) -> dytnsapi_20200217_models.InvalidPhoneNumberFilterResponse:
        """
        @summary Filters invalid phone numbers.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click *Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 1,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: InvalidPhoneNumberFilterRequest
        @return: InvalidPhoneNumberFilterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.invalid_phone_number_filter_with_options(request, runtime)

    async def invalid_phone_number_filter_async(
        self,
        request: dytnsapi_20200217_models.InvalidPhoneNumberFilterRequest,
    ) -> dytnsapi_20200217_models.InvalidPhoneNumberFilterResponse:
        """
        @summary Filters invalid phone numbers.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click *Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 1,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: InvalidPhoneNumberFilterRequest
        @return: InvalidPhoneNumberFilterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.invalid_phone_number_filter_with_options_async(request, runtime)

    def phone_number_convert_service_with_options(
        self,
        request: dytnsapi_20200217_models.PhoneNumberConvertServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberConvertServiceResponse:
        """
        @param request: PhoneNumberConvertServiceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberConvertServiceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberConvertService',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberConvertServiceResponse(),
            self.call_api(params, req, runtime)
        )

    async def phone_number_convert_service_with_options_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberConvertServiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberConvertServiceResponse:
        """
        @param request: PhoneNumberConvertServiceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberConvertServiceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberConvertService',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberConvertServiceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def phone_number_convert_service(
        self,
        request: dytnsapi_20200217_models.PhoneNumberConvertServiceRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberConvertServiceResponse:
        """
        @param request: PhoneNumberConvertServiceRequest
        @return: PhoneNumberConvertServiceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.phone_number_convert_service_with_options(request, runtime)

    async def phone_number_convert_service_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberConvertServiceRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberConvertServiceResponse:
        """
        @param request: PhoneNumberConvertServiceRequest
        @return: PhoneNumberConvertServiceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.phone_number_convert_service_with_options_async(request, runtime)

    def phone_number_encrypt_with_options(
        self,
        request: dytnsapi_20200217_models.PhoneNumberEncryptRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberEncryptResponse:
        """
        @summary Encrypts the original phone number into a virtual number that starts with 140. Cell Phone Number Service integrates the communications services provided by Alibaba Cloud. This allows you to initiate a call by using a virtual number that starts with 140.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click *Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 1,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberEncryptRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberEncryptResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberEncrypt',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberEncryptResponse(),
            self.call_api(params, req, runtime)
        )

    async def phone_number_encrypt_with_options_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberEncryptRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberEncryptResponse:
        """
        @summary Encrypts the original phone number into a virtual number that starts with 140. Cell Phone Number Service integrates the communications services provided by Alibaba Cloud. This allows you to initiate a call by using a virtual number that starts with 140.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click *Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 1,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberEncryptRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberEncryptResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberEncrypt',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberEncryptResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def phone_number_encrypt(
        self,
        request: dytnsapi_20200217_models.PhoneNumberEncryptRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberEncryptResponse:
        """
        @summary Encrypts the original phone number into a virtual number that starts with 140. Cell Phone Number Service integrates the communications services provided by Alibaba Cloud. This allows you to initiate a call by using a virtual number that starts with 140.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click *Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 1,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberEncryptRequest
        @return: PhoneNumberEncryptResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.phone_number_encrypt_with_options(request, runtime)

    async def phone_number_encrypt_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberEncryptRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberEncryptResponse:
        """
        @summary Encrypts the original phone number into a virtual number that starts with 140. Cell Phone Number Service integrates the communications services provided by Alibaba Cloud. This allows you to initiate a call by using a virtual number that starts with 140.
        
        @description Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click *Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 1,000 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberEncryptRequest
        @return: PhoneNumberEncryptResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.phone_number_encrypt_with_options_async(request, runtime)

    def phone_number_status_for_account_with_options(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForAccountRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForAccountResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForAccountRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForAccountResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForAccount',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForAccountResponse(),
            self.call_api(params, req, runtime)
        )

    async def phone_number_status_for_account_with_options_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForAccountRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForAccountResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForAccountRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForAccountResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForAccount',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForAccountResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def phone_number_status_for_account(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForAccountRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForAccountResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForAccountRequest
        @return: PhoneNumberStatusForAccountResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.phone_number_status_for_account_with_options(request, runtime)

    async def phone_number_status_for_account_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForAccountRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForAccountResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForAccountRequest
        @return: PhoneNumberStatusForAccountResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.phone_number_status_for_account_with_options_async(request, runtime)

    def phone_number_status_for_public_with_options(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForPublicRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForPublicResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForPublicRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForPublicResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForPublic',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForPublicResponse(),
            self.call_api(params, req, runtime)
        )

    async def phone_number_status_for_public_with_options_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForPublicRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForPublicResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForPublicRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForPublicResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForPublic',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForPublicResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def phone_number_status_for_public(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForPublicRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForPublicResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForPublicRequest
        @return: PhoneNumberStatusForPublicResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.phone_number_status_for_public_with_options(request, runtime)

    async def phone_number_status_for_public_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForPublicRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForPublicResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForPublicRequest
        @return: PhoneNumberStatusForPublicResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.phone_number_status_for_public_with_options_async(request, runtime)

    def phone_number_status_for_real_with_options(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForRealRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForRealResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForRealRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForRealResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForReal',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForRealResponse(),
            self.call_api(params, req, runtime)
        )

    async def phone_number_status_for_real_with_options_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForRealRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForRealResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForRealRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForRealResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForReal',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForRealResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def phone_number_status_for_real(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForRealRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForRealResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForRealRequest
        @return: PhoneNumberStatusForRealResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.phone_number_status_for_real_with_options(request, runtime)

    async def phone_number_status_for_real_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForRealRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForRealResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForRealRequest
        @return: PhoneNumberStatusForRealResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.phone_number_status_for_real_with_options_async(request, runtime)

    def phone_number_status_for_sms_with_options(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForSmsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForSmsResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForSmsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForSmsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForSms',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForSmsResponse(),
            self.call_api(params, req, runtime)
        )

    async def phone_number_status_for_sms_with_options_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForSmsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForSmsResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForSmsRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForSmsResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForSms',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForSmsResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def phone_number_status_for_sms(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForSmsRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForSmsResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForSmsRequest
        @return: PhoneNumberStatusForSmsResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.phone_number_status_for_sms_with_options(request, runtime)

    async def phone_number_status_for_sms_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForSmsRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForSmsResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForSmsRequest
        @return: PhoneNumberStatusForSmsResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.phone_number_status_for_sms_with_options_async(request, runtime)

    def phone_number_status_for_voice_with_options(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForVoiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForVoiceResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForVoiceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForVoiceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForVoice',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForVoiceResponse(),
            self.call_api(params, req, runtime)
        )

    async def phone_number_status_for_voice_with_options_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForVoiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForVoiceResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForVoiceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: PhoneNumberStatusForVoiceResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='PhoneNumberStatusForVoice',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.PhoneNumberStatusForVoiceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def phone_number_status_for_voice(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForVoiceRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForVoiceResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForVoiceRequest
        @return: PhoneNumberStatusForVoiceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.phone_number_status_for_voice_with_options(request, runtime)

    async def phone_number_status_for_voice_async(
        self,
        request: dytnsapi_20200217_models.PhoneNumberStatusForVoiceRequest,
    ) -> dytnsapi_20200217_models.PhoneNumberStatusForVoiceResponse:
        """
        @summary Queries the real-time service state of a phone number. The state includes NORMAL, SHUTDOWN, and NOT_EXIST. You can choose an encryption method for your phone number query, including plaintext, MD5, and SHA256.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        By default, only Alibaba Cloud accounts can call this operation. RAM users can call this operation only after the RAM users are granted the related permissions. For more information, see [Grant permissions to RAM users](https://help.aliyun.com/document_detail/154006.html).
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        ### [](#qps)QPS limits
        You can call this operation up to 300 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: PhoneNumberStatusForVoiceRequest
        @return: PhoneNumberStatusForVoiceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.phone_number_status_for_voice_with_options_async(request, runtime)

    def query_available_auth_code_with_options(
        self,
        request: dytnsapi_20200217_models.QueryAvailableAuthCodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryAvailableAuthCodeResponse:
        """
        @summary Queries available authorization codes.
        
        @param request: QueryAvailableAuthCodeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryAvailableAuthCodeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.tag_id):
            query['TagId'] = request.tag_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryAvailableAuthCode',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryAvailableAuthCodeResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_available_auth_code_with_options_async(
        self,
        request: dytnsapi_20200217_models.QueryAvailableAuthCodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryAvailableAuthCodeResponse:
        """
        @summary Queries available authorization codes.
        
        @param request: QueryAvailableAuthCodeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryAvailableAuthCodeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.tag_id):
            query['TagId'] = request.tag_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryAvailableAuthCode',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryAvailableAuthCodeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_available_auth_code(
        self,
        request: dytnsapi_20200217_models.QueryAvailableAuthCodeRequest,
    ) -> dytnsapi_20200217_models.QueryAvailableAuthCodeResponse:
        """
        @summary Queries available authorization codes.
        
        @param request: QueryAvailableAuthCodeRequest
        @return: QueryAvailableAuthCodeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.query_available_auth_code_with_options(request, runtime)

    async def query_available_auth_code_async(
        self,
        request: dytnsapi_20200217_models.QueryAvailableAuthCodeRequest,
    ) -> dytnsapi_20200217_models.QueryAvailableAuthCodeResponse:
        """
        @summary Queries available authorization codes.
        
        @param request: QueryAvailableAuthCodeRequest
        @return: QueryAvailableAuthCodeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.query_available_auth_code_with_options_async(request, runtime)

    def query_phone_number_online_time_with_options(
        self,
        request: dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeResponse:
        """
        @summary 在网时长专用接口
        
        @param request: QueryPhoneNumberOnlineTimeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryPhoneNumberOnlineTimeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryPhoneNumberOnlineTime',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_phone_number_online_time_with_options_async(
        self,
        request: dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeResponse:
        """
        @summary 在网时长专用接口
        
        @param request: QueryPhoneNumberOnlineTimeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryPhoneNumberOnlineTimeResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryPhoneNumberOnlineTime',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_phone_number_online_time(
        self,
        request: dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeRequest,
    ) -> dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeResponse:
        """
        @summary 在网时长专用接口
        
        @param request: QueryPhoneNumberOnlineTimeRequest
        @return: QueryPhoneNumberOnlineTimeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.query_phone_number_online_time_with_options(request, runtime)

    async def query_phone_number_online_time_async(
        self,
        request: dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeRequest,
    ) -> dytnsapi_20200217_models.QueryPhoneNumberOnlineTimeResponse:
        """
        @summary 在网时长专用接口
        
        @param request: QueryPhoneNumberOnlineTimeRequest
        @return: QueryPhoneNumberOnlineTimeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.query_phone_number_online_time_with_options_async(request, runtime)

    def query_phone_twice_tel_verify_with_options(
        self,
        request: dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyResponse:
        """
        @summary 二次号携号转网号码查询
        
        @param request: QueryPhoneTwiceTelVerifyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryPhoneTwiceTelVerifyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryPhoneTwiceTelVerify',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_phone_twice_tel_verify_with_options_async(
        self,
        request: dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyResponse:
        """
        @summary 二次号携号转网号码查询
        
        @param request: QueryPhoneTwiceTelVerifyRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryPhoneTwiceTelVerifyResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.start_time):
            query['StartTime'] = request.start_time
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryPhoneTwiceTelVerify',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_phone_twice_tel_verify(
        self,
        request: dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyRequest,
    ) -> dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyResponse:
        """
        @summary 二次号携号转网号码查询
        
        @param request: QueryPhoneTwiceTelVerifyRequest
        @return: QueryPhoneTwiceTelVerifyResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.query_phone_twice_tel_verify_with_options(request, runtime)

    async def query_phone_twice_tel_verify_async(
        self,
        request: dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyRequest,
    ) -> dytnsapi_20200217_models.QueryPhoneTwiceTelVerifyResponse:
        """
        @summary 二次号携号转网号码查询
        
        @param request: QueryPhoneTwiceTelVerifyRequest
        @return: QueryPhoneTwiceTelVerifyResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.query_phone_twice_tel_verify_with_options_async(request, runtime)

    def query_tag_apply_rule_with_options(
        self,
        request: dytnsapi_20200217_models.QueryTagApplyRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryTagApplyRuleResponse:
        """
        @summary Queries tag application rules.
        
        @param request: QueryTagApplyRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryTagApplyRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.tag_id):
            query['TagId'] = request.tag_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryTagApplyRule',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryTagApplyRuleResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_tag_apply_rule_with_options_async(
        self,
        request: dytnsapi_20200217_models.QueryTagApplyRuleRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryTagApplyRuleResponse:
        """
        @summary Queries tag application rules.
        
        @param request: QueryTagApplyRuleRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryTagApplyRuleResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.tag_id):
            query['TagId'] = request.tag_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryTagApplyRule',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryTagApplyRuleResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_tag_apply_rule(
        self,
        request: dytnsapi_20200217_models.QueryTagApplyRuleRequest,
    ) -> dytnsapi_20200217_models.QueryTagApplyRuleResponse:
        """
        @summary Queries tag application rules.
        
        @param request: QueryTagApplyRuleRequest
        @return: QueryTagApplyRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.query_tag_apply_rule_with_options(request, runtime)

    async def query_tag_apply_rule_async(
        self,
        request: dytnsapi_20200217_models.QueryTagApplyRuleRequest,
    ) -> dytnsapi_20200217_models.QueryTagApplyRuleResponse:
        """
        @summary Queries tag application rules.
        
        @param request: QueryTagApplyRuleRequest
        @return: QueryTagApplyRuleResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.query_tag_apply_rule_with_options_async(request, runtime)

    def query_tag_info_by_selection_with_options(
        self,
        request: dytnsapi_20200217_models.QueryTagInfoBySelectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryTagInfoBySelectionResponse:
        """
        @summary Queries information about tags.
        
        @param request: QueryTagInfoBySelectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryTagInfoBySelectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.industry_id):
            query['IndustryId'] = request.industry_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scene_id):
            query['SceneId'] = request.scene_id
        if not UtilClient.is_unset(request.tag_id):
            query['TagId'] = request.tag_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryTagInfoBySelection',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryTagInfoBySelectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_tag_info_by_selection_with_options_async(
        self,
        request: dytnsapi_20200217_models.QueryTagInfoBySelectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryTagInfoBySelectionResponse:
        """
        @summary Queries information about tags.
        
        @param request: QueryTagInfoBySelectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryTagInfoBySelectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.industry_id):
            query['IndustryId'] = request.industry_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.scene_id):
            query['SceneId'] = request.scene_id
        if not UtilClient.is_unset(request.tag_id):
            query['TagId'] = request.tag_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryTagInfoBySelection',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryTagInfoBySelectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_tag_info_by_selection(
        self,
        request: dytnsapi_20200217_models.QueryTagInfoBySelectionRequest,
    ) -> dytnsapi_20200217_models.QueryTagInfoBySelectionResponse:
        """
        @summary Queries information about tags.
        
        @param request: QueryTagInfoBySelectionRequest
        @return: QueryTagInfoBySelectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.query_tag_info_by_selection_with_options(request, runtime)

    async def query_tag_info_by_selection_async(
        self,
        request: dytnsapi_20200217_models.QueryTagInfoBySelectionRequest,
    ) -> dytnsapi_20200217_models.QueryTagInfoBySelectionResponse:
        """
        @summary Queries information about tags.
        
        @param request: QueryTagInfoBySelectionRequest
        @return: QueryTagInfoBySelectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.query_tag_info_by_selection_with_options_async(request, runtime)

    def query_tag_list_page_with_options(
        self,
        request: dytnsapi_20200217_models.QueryTagListPageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryTagListPageResponse:
        """
        @summary Queries a list of tags by page.
        
        @param request: QueryTagListPageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryTagListPageResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.page_no):
            query['PageNo'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryTagListPage',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryTagListPageResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_tag_list_page_with_options_async(
        self,
        request: dytnsapi_20200217_models.QueryTagListPageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryTagListPageResponse:
        """
        @summary Queries a list of tags by page.
        
        @param request: QueryTagListPageRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryTagListPageResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.page_no):
            query['PageNo'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryTagListPage',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryTagListPageResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_tag_list_page(
        self,
        request: dytnsapi_20200217_models.QueryTagListPageRequest,
    ) -> dytnsapi_20200217_models.QueryTagListPageResponse:
        """
        @summary Queries a list of tags by page.
        
        @param request: QueryTagListPageRequest
        @return: QueryTagListPageResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.query_tag_list_page_with_options(request, runtime)

    async def query_tag_list_page_async(
        self,
        request: dytnsapi_20200217_models.QueryTagListPageRequest,
    ) -> dytnsapi_20200217_models.QueryTagListPageResponse:
        """
        @summary Queries a list of tags by page.
        
        @param request: QueryTagListPageRequest
        @return: QueryTagListPageResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.query_tag_list_page_with_options_async(request, runtime)

    def query_usage_statistics_by_tag_id_with_options(
        self,
        request: dytnsapi_20200217_models.QueryUsageStatisticsByTagIdRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryUsageStatisticsByTagIdResponse:
        """
        @summary Queries the usage statistics based on tag IDs.
        
        @param request: QueryUsageStatisticsByTagIdRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryUsageStatisticsByTagIdResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.begin_time):
            query['BeginTime'] = request.begin_time
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.page_no):
            query['PageNo'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.tag_id):
            query['TagId'] = request.tag_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryUsageStatisticsByTagId',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryUsageStatisticsByTagIdResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_usage_statistics_by_tag_id_with_options_async(
        self,
        request: dytnsapi_20200217_models.QueryUsageStatisticsByTagIdRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.QueryUsageStatisticsByTagIdResponse:
        """
        @summary Queries the usage statistics based on tag IDs.
        
        @param request: QueryUsageStatisticsByTagIdRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryUsageStatisticsByTagIdResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.begin_time):
            query['BeginTime'] = request.begin_time
        if not UtilClient.is_unset(request.end_time):
            query['EndTime'] = request.end_time
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.page_no):
            query['PageNo'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['PageSize'] = request.page_size
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.tag_id):
            query['TagId'] = request.tag_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryUsageStatisticsByTagId',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.QueryUsageStatisticsByTagIdResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_usage_statistics_by_tag_id(
        self,
        request: dytnsapi_20200217_models.QueryUsageStatisticsByTagIdRequest,
    ) -> dytnsapi_20200217_models.QueryUsageStatisticsByTagIdResponse:
        """
        @summary Queries the usage statistics based on tag IDs.
        
        @param request: QueryUsageStatisticsByTagIdRequest
        @return: QueryUsageStatisticsByTagIdResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.query_usage_statistics_by_tag_id_with_options(request, runtime)

    async def query_usage_statistics_by_tag_id_async(
        self,
        request: dytnsapi_20200217_models.QueryUsageStatisticsByTagIdRequest,
    ) -> dytnsapi_20200217_models.QueryUsageStatisticsByTagIdResponse:
        """
        @summary Queries the usage statistics based on tag IDs.
        
        @param request: QueryUsageStatisticsByTagIdRequest
        @return: QueryUsageStatisticsByTagIdResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.query_usage_statistics_by_tag_id_with_options_async(request, runtime)

    def three_elements_verification_with_options(
        self,
        request: dytnsapi_20200217_models.ThreeElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.ThreeElementsVerificationResponse:
        """
        @summary Verifies whether the name, phone number, and ID card number entered by a user belong to the same user.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        You are charged only if the value of Code is OK and the value of IsConsistent is not 2.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: ThreeElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ThreeElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.cert_code):
            query['CertCode'] = request.cert_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ThreeElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.ThreeElementsVerificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def three_elements_verification_with_options_async(
        self,
        request: dytnsapi_20200217_models.ThreeElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.ThreeElementsVerificationResponse:
        """
        @summary Verifies whether the name, phone number, and ID card number entered by a user belong to the same user.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        You are charged only if the value of Code is OK and the value of IsConsistent is not 2.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: ThreeElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ThreeElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.cert_code):
            query['CertCode'] = request.cert_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ThreeElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.ThreeElementsVerificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def three_elements_verification(
        self,
        request: dytnsapi_20200217_models.ThreeElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.ThreeElementsVerificationResponse:
        """
        @summary Verifies whether the name, phone number, and ID card number entered by a user belong to the same user.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        You are charged only if the value of Code is OK and the value of IsConsistent is not 2.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: ThreeElementsVerificationRequest
        @return: ThreeElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.three_elements_verification_with_options(request, runtime)

    async def three_elements_verification_async(
        self,
        request: dytnsapi_20200217_models.ThreeElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.ThreeElementsVerificationResponse:
        """
        @summary Verifies whether the name, phone number, and ID card number entered by a user belong to the same user.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        You are charged only if the value of Code is OK and the value of IsConsistent is not 2.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: ThreeElementsVerificationRequest
        @return: ThreeElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.three_elements_verification_with_options_async(request, runtime)

    def two_elements_verification_with_options(
        self,
        request: dytnsapi_20200217_models.TwoElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.TwoElementsVerificationResponse:
        """
        @summary Verifies whether the name and phone number entered by a user belong to the same user.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        You are charged only if the value of Code is OK and the value of IsConsistent is not 2.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: TwoElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: TwoElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TwoElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.TwoElementsVerificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def two_elements_verification_with_options_async(
        self,
        request: dytnsapi_20200217_models.TwoElementsVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.TwoElementsVerificationResponse:
        """
        @summary Verifies whether the name and phone number entered by a user belong to the same user.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        You are charged only if the value of Code is OK and the value of IsConsistent is not 2.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: TwoElementsVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: TwoElementsVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.input_number):
            query['InputNumber'] = request.input_number
        if not UtilClient.is_unset(request.mask):
            query['Mask'] = request.mask
        if not UtilClient.is_unset(request.name):
            query['Name'] = request.name
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TwoElementsVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.TwoElementsVerificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def two_elements_verification(
        self,
        request: dytnsapi_20200217_models.TwoElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.TwoElementsVerificationResponse:
        """
        @summary Verifies whether the name and phone number entered by a user belong to the same user.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        You are charged only if the value of Code is OK and the value of IsConsistent is not 2.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: TwoElementsVerificationRequest
        @return: TwoElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.two_elements_verification_with_options(request, runtime)

    async def two_elements_verification_async(
        self,
        request: dytnsapi_20200217_models.TwoElementsVerificationRequest,
    ) -> dytnsapi_20200217_models.TwoElementsVerificationResponse:
        """
        @summary Verifies whether the name and phone number entered by a user belong to the same user.
        
        @description    Before you call this operation, make sure that you are familiar with the [billing](https://help.aliyun.com/document_detail/154751.html) of Cell Phone Number Service.
        Before you call this operation, perform the following operations: Log on to the Cell Phone Number Service console. On the [Labels](https://dytns.console.aliyun.com/analysis/square) page, find the label that you want to use, click **Activate Now**, enter the required information, and then submit your application. After your application is approved, you can use the label.
        You are charged only if the value of Code is OK and the value of IsConsistent is not 2.
        ### [](#qps)QPS limits
        You can call this operation up to 200 times per second per account. If the number of calls per second exceeds the limit, throttling is triggered. As a result, your business may be affected. We recommend that you take note of the limit when you call this operation.
        
        @param request: TwoElementsVerificationRequest
        @return: TwoElementsVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.two_elements_verification_with_options_async(request, runtime)

    def u_aidcollection_with_options(
        self,
        request: dytnsapi_20200217_models.UAIDCollectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.UAIDCollectionResponse:
        """
        @summary UAID采集
        
        @param request: UAIDCollectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UAIDCollectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.ip):
            query['Ip'] = request.ip
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.province):
            query['Province'] = request.province
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        if not UtilClient.is_unset(request.user_grant_id):
            query['UserGrantId'] = request.user_grant_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UAIDCollection',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.UAIDCollectionResponse(),
            self.call_api(params, req, runtime)
        )

    async def u_aidcollection_with_options_async(
        self,
        request: dytnsapi_20200217_models.UAIDCollectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.UAIDCollectionResponse:
        """
        @summary UAID采集
        
        @param request: UAIDCollectionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UAIDCollectionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.ip):
            query['Ip'] = request.ip
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.province):
            query['Province'] = request.province
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        if not UtilClient.is_unset(request.user_grant_id):
            query['UserGrantId'] = request.user_grant_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UAIDCollection',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.UAIDCollectionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def u_aidcollection(
        self,
        request: dytnsapi_20200217_models.UAIDCollectionRequest,
    ) -> dytnsapi_20200217_models.UAIDCollectionResponse:
        """
        @summary UAID采集
        
        @param request: UAIDCollectionRequest
        @return: UAIDCollectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.u_aidcollection_with_options(request, runtime)

    async def u_aidcollection_async(
        self,
        request: dytnsapi_20200217_models.UAIDCollectionRequest,
    ) -> dytnsapi_20200217_models.UAIDCollectionResponse:
        """
        @summary UAID采集
        
        @param request: UAIDCollectionRequest
        @return: UAIDCollectionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.u_aidcollection_with_options_async(request, runtime)

    def u_aidconversion_with_options(
        self,
        request: dytnsapi_20200217_models.UAIDConversionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.UAIDConversionResponse:
        """
        @summary uaid号码转换服务
        
        @param request: UAIDConversionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UAIDConversionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.uaid_list):
            query['UaidList'] = request.uaid_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UAIDConversion',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.UAIDConversionResponse(),
            self.call_api(params, req, runtime)
        )

    async def u_aidconversion_with_options_async(
        self,
        request: dytnsapi_20200217_models.UAIDConversionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.UAIDConversionResponse:
        """
        @summary uaid号码转换服务
        
        @param request: UAIDConversionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UAIDConversionResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.uaid_list):
            query['UaidList'] = request.uaid_list
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UAIDConversion',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.UAIDConversionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def u_aidconversion(
        self,
        request: dytnsapi_20200217_models.UAIDConversionRequest,
    ) -> dytnsapi_20200217_models.UAIDConversionResponse:
        """
        @summary uaid号码转换服务
        
        @param request: UAIDConversionRequest
        @return: UAIDConversionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.u_aidconversion_with_options(request, runtime)

    async def u_aidconversion_async(
        self,
        request: dytnsapi_20200217_models.UAIDConversionRequest,
    ) -> dytnsapi_20200217_models.UAIDConversionResponse:
        """
        @summary uaid号码转换服务
        
        @param request: UAIDConversionRequest
        @return: UAIDConversionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.u_aidconversion_with_options_async(request, runtime)

    def u_aidverification_with_options(
        self,
        request: dytnsapi_20200217_models.UAIDVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.UAIDVerificationResponse:
        """
        @summary 获取UAID
        
        @param request: UAIDVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UAIDVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.ip):
            query['Ip'] = request.ip
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.province):
            query['Province'] = request.province
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        if not UtilClient.is_unset(request.user_grant_id):
            query['UserGrantId'] = request.user_grant_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UAIDVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.UAIDVerificationResponse(),
            self.call_api(params, req, runtime)
        )

    async def u_aidverification_with_options_async(
        self,
        request: dytnsapi_20200217_models.UAIDVerificationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> dytnsapi_20200217_models.UAIDVerificationResponse:
        """
        @summary 获取UAID
        
        @param request: UAIDVerificationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UAIDVerificationResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.auth_code):
            query['AuthCode'] = request.auth_code
        if not UtilClient.is_unset(request.carrier):
            query['Carrier'] = request.carrier
        if not UtilClient.is_unset(request.ip):
            query['Ip'] = request.ip
        if not UtilClient.is_unset(request.out_id):
            query['OutId'] = request.out_id
        if not UtilClient.is_unset(request.owner_id):
            query['OwnerId'] = request.owner_id
        if not UtilClient.is_unset(request.province):
            query['Province'] = request.province
        if not UtilClient.is_unset(request.resource_owner_account):
            query['ResourceOwnerAccount'] = request.resource_owner_account
        if not UtilClient.is_unset(request.resource_owner_id):
            query['ResourceOwnerId'] = request.resource_owner_id
        if not UtilClient.is_unset(request.token):
            query['Token'] = request.token
        if not UtilClient.is_unset(request.user_grant_id):
            query['UserGrantId'] = request.user_grant_id
        req = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UAIDVerification',
            version='2020-02-17',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            dytnsapi_20200217_models.UAIDVerificationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def u_aidverification(
        self,
        request: dytnsapi_20200217_models.UAIDVerificationRequest,
    ) -> dytnsapi_20200217_models.UAIDVerificationResponse:
        """
        @summary 获取UAID
        
        @param request: UAIDVerificationRequest
        @return: UAIDVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.u_aidverification_with_options(request, runtime)

    async def u_aidverification_async(
        self,
        request: dytnsapi_20200217_models.UAIDVerificationRequest,
    ) -> dytnsapi_20200217_models.UAIDVerificationResponse:
        """
        @summary 获取UAID
        
        @param request: UAIDVerificationRequest
        @return: UAIDVerificationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.u_aidverification_with_options_async(request, runtime)
