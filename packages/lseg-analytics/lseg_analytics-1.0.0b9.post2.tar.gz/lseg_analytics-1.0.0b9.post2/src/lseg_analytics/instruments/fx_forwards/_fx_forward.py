import copy
import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from lseg_analytics._client.client import Client
from lseg_analytics.common._resource_base import ResourceBase
from lseg_analytics.exceptions import (
    LibraryException,
    ResourceNotFound,
    check_and_raise,
    check_exception_and_raise,
)
from lseg_analytics_basic_client.models import (
    Description,
    FxForwardAnalyticsPricing,
    FxForwardAnalyticsValuation,
    FxForwardAsCollectionItem,
    FxForwardInstrument,
    Location,
    MarketDataInput,
    PricingParameters,
    ResourceType,
)

from ._logger import logger


class FxForward(ResourceBase):
    """
    FxForward object.

    Contains all the necessary information to identify and define a FxForward instance.

    Attributes
    ----------
    type : Union[str, ResourceType], optional
        The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str, optional
        A resource ID is the unique resource identifier for an object on the platform. The resource ID is created on saving. IDs are read-only.
    location : Location
        Name and space are location attributes, which are automatically set when a resource object is saved for the first time. Unsaved resources have thier name and space set to None. Location attributes are read-only.
    description : Description, optional
        Description object that contains the resource summary and tags.
    definition : FxForwardInstrument
        The definition of a FX forward instrument.

    See Also
    --------
    FxForward.price : Price a FX Forward Instrument (pre-trade). Currently, only NextBusinessDay is supported for the date moving convention in the start date or end date.
    FxForward.value : Valuate a FX Forward Instrument (post-trade). Currently, only NextBusinessDay is supported for the date moving convention in the start date or end date.

    Examples
    --------
    Create a FxForward instance.

    >>> fx_forward = FxForward(
    >>>     FxForwardInstrument(
    >>>         fx_rate=FxRate(cross_currency=CrossCurrencyInput(code="USDEUR"), rate=1.05),
    >>>         end_date=AdjustableDate(date_moving_convention=DateMovingConvention.NEXT_BUSINESS_DAY),
    >>>     )
    >>> )

    Save the instance with name and space.

    >>> fx_forward.save(name="MyCurve", space="MySpace")
    True

    """

    _definition_class = FxForwardInstrument

    def __init__(self, definition: FxForwardInstrument, description: Optional[Description] = None):
        """
        FxForward constructor

        Parameters
        ----------
        definition : FxForwardInstrument
            The definition of a FX forward instrument.
        description : Description, optional
            Description object that contains the resource summary and tags.

        Examples
        --------
        Create a FxForward instance.

        >>> fx_forward = FxForward(
        >>>     FxForwardInstrument(
        >>>         fx_rate=FxRate(cross_currency=CrossCurrencyInput(code="USDEUR"), rate=1.05),
        >>>         end_date=AdjustableDate(date_moving_convention=DateMovingConvention.NEXT_BUSINESS_DAY),
        >>>     )
        >>> )

        """
        self.definition: FxForwardInstrument = definition
        self.type: Optional[Union[str, ResourceType]] = "FxForward"
        if description is None:
            self.description: Optional[Description] = Description(tags=[])
        else:
            self.description: Optional[Description] = description
        self._location: Location = Location(name="")
        self._id: Optional[str] = None

    @property
    def id(self):
        """
        Returns the FxForward id

        Parameters
        ----------


        Returns
        --------
        str
            A resource ID is the unique resource identifier for an object on the platform. The resource ID is created on saving. IDs are read-only.

        Examples
        --------
        Get the instance id.

        >>> fx_forward.id
        '985B1CUR-6EE9-4B1F-870F-5BA89EBE71EG'

        """
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("id is read only")

    @property
    def location(self):
        """
        Returns the FxForward location

        Parameters
        ----------


        Returns
        --------
        Location
            Name and space are location attributes, which are automatically set when a resource object is saved for the first time. Unsaved resources have thier name and space set to None. Location attributes are read-only.

        Examples
        --------
        Get the location property.

        >>> fx_forward.location.name
        'EURGBP'


        >>> fx_forward.location.space
        'MYSPACE'

        """
        return self._location

    @location.setter
    def location(self, value):
        raise AttributeError("location is read only")

    def _create(self, location: Location) -> None:
        """
        Create resource.

        Parameters
        ----------
        location : Location
            Name and space are location attributes, which are automatically set when a resource object is saved for the first time. Unsaved resources have thier name and space set to None. Location attributes are read-only.

        Returns
        --------
        None


        Examples
        --------


        """

        try:
            logger.info(f"Creating FxForwardResource")

            response = check_and_raise(
                Client().fx_forwards_resource.create(
                    location=location,
                    description=self.description,
                    definition=self.definition,
                )
            )

            self._id = response.data.id

            self._location = response.data.location
            logger.info(f"FxForwardResource created with id: {self._id}")
        except Exception as err:
            logger.error(f"Error creating FxForwardResource: {err}")
            raise err

    def _overwrite(self) -> None:
        """
        Overwrite resource

        Parameters
        ----------


        Returns
        --------
        None


        Examples
        --------


        """
        logger.info(f"Overwriting FxForwardResource with id: {self._id}")
        check_and_raise(
            Client().fx_forward_resource.overwrite(
                instrument_id=self._id,
                location=self._location,
                description=self.description,
                definition=self.definition,
            )
        )

    def price(
        self,
        *,
        parameters: Optional[PricingParameters] = None,
        market_data: Optional[MarketDataInput] = None,
    ) -> FxForwardAnalyticsPricing:
        """
        Price a FX Forward Instrument (pre-trade). Currently, only NextBusinessDay is supported for the date moving convention in the start date or end date.

        Parameters
        ----------
        parameters : PricingParameters, optional
            Base cross asset calculation parameters.
        market_data : MarketDataInput, optional
            An object defining market data to be used to compute the analytics.

        Returns
        --------
        FxForwardAnalyticsPricing
            Object defining the output of a FX Forward pricing analysis.

        Examples
        --------
        Calling price on a FxForward instance

        >>> fx_forward_client.price()
        {'description': {'endDate': {'adjusted': '2023-04-14', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': '', 'referenceDate': 'SpotDate', 'tenor': '6M', 'unAdjusted': '2023-04-14'}, 'startDate': {'adjusted': '2022-10-14', 'date': '2022-10-14', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': '', 'referenceDate': 'ValuationDate', 'unAdjusted': '2022-10-14'}, 'valuationDate': '2022-10-12'}, 'greeks': {'deltaAmountInContraCcy': 1984832.58230644, 'deltaAmountInDealCcy': 1985823.52830793, 'deltaAmountInReportCcy': None, 'deltaPercent': 99.241629115322}, 'pricingAnalysis': {'contraAmount': 1969900, 'dealAmount': 2000000, 'discountFactor': 0.99241629115322, 'fxOutrightCcy1Ccy2': {'ask': 0.98495, 'bid': 0.983967}, 'fxSpot': {'ask': 0.9708, 'bid': 0.9704}, 'fxSwapsCcy1': {'ask': 141.5, 'bid': 135.67}, 'fxSwapsCcy1Ccy2': {'ask': 141.49999999999997, 'bid': 135.66999999999996}, 'fxSwapsCcy2': {'ask': 0, 'bid': 0}, 'tradedCrossRate': 0.98495}}

        Calling price on a FxForward instance with parameters.

        >>> fx_forward_client.price(
        >>>     parameters=PricingParameters(
        >>>         valuation_date=datetime.date(2022, 10, 12),
        >>>         fx_pricing_preferences=FxPricingPreferences(
        >>>             ignore_reference_currency_holidays=True,
        >>>             reference_currency=CurrencyInput(code="USD"),
        >>>             report_currency=CurrencyInput(code="USD"),
        >>>         ),
        >>>     ),
        >>>     market_data=MarketDataInput(
        >>>         fx_forward_curves=[FxForwardCurveAsMarketDataInput(cross_currency=CrossCurrencyInput(code="USD"))]
        >>>     )
        >>> )
        {'description': {'endDate': {'adjusted': '2023-04-14', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': '', 'referenceDate': 'SpotDate', 'tenor': '6M', 'unAdjusted': '2023-04-14'}, 'startDate': {'adjusted': '2022-10-14', 'date': '2022-10-14', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': '', 'referenceDate': 'ValuationDate', 'unAdjusted': '2022-10-14'}, 'valuationDate': '2022-10-12'}, 'greeks': {'deltaAmountInContraCcy': 1984832.58230644, 'deltaAmountInDealCcy': 1985823.52830793, 'deltaAmountInReportCcy': None, 'deltaPercent': 99.241629115322}, 'pricingAnalysis': {'contraAmount': 1969900, 'dealAmount': 2000000, 'discountFactor': 0.99241629115322, 'fxOutrightCcy1Ccy2': {'ask': 0.98495, 'bid': 0.983967}, 'fxSpot': {'ask': 0.9708, 'bid': 0.9704}, 'fxSwapsCcy1': {'ask': 141.5, 'bid': 135.67}, 'fxSwapsCcy1Ccy2': {'ask': 141.49999999999997, 'bid': 135.66999999999996}, 'fxSwapsCcy2': {'ask': 0, 'bid': 0}, 'tradedCrossRate': 0.98495}}

        Calling price on a FxForward instance with parameters, using a definition of a pre-loaded curve.

        >>> eurgbp_curve = load(space='LSEG', name='EUR CAD FxForward')
        >>> eurgbp_fxfwd = FxForward(
        >>>     definition=(FxForwardInstrument(
        >>>     fx_rate=FxRate(cross_currency="EURCAD", rate=0.9),
        >>>     end_date=RelativeAdjustableDate(tenor="4M"),
        >>>     start_date=RelativeAdjustableDate(tenor="2M"),
        >>>     deal_amount=34000
        >>>     )
        >>>     ))
        >>> market_data = MarketDataInput()
        >>> market_data.fx_forward_curves.append(eurgbp_curve.definition)
        >>> eurgbp_fxfwd.price(market_data=market_data)
        {'description': {'valuationDate': '2025-01-15', 'startDate': {'unAdjusted': '2025-03-17', 'adjusted': '2025-03-17', 'dateMovingConvention': 'NextBusinessDay', 'tenor': '2M'}, 'endDate': {'unAdjusted': '2025-05-17', 'adjusted': '2025-05-20', 'dateMovingConvention': 'NextBusinessDay', 'tenor': '4M'}}, 'pricingAnalysis': {'fxSwapsCcy1': {'bid': 0.0, 'ask': 0.0}, 'fxSwapsCcy2': {'bid': 12.010000000000076, 'ask': 13.780000000001014}, 'fxSwapsCcy1Ccy2': {'bid': 12.010000000000076, 'ask': 13.780000000001014}, 'fxOutrightCcy1Ccy2': {'bid': 1.479551, 'ask': 1.480002}, 'tradedCrossRate': 0.9, 'fxSpot': {'bid': 1.4777, 'ask': 1.478}, 'dealAmount': 34000.0, 'contraAmount': 30600.0}, 'greeks': {'deltaPercent': 99.5342423105718, 'deltaAmountInDealCcy': 20582.485359806, 'deltaAmountInContraCcy': 33841.6423855944}}

        """

        try:

            response = None

            if self._id:

                response = check_and_raise(
                    Client().fx_forward_resource.price(
                        instrument_id=self._id,
                        parameters=parameters,
                        market_data=market_data,
                    )
                )
            else:

                response = check_and_raise(
                    Client().fx_forwards_resource.price(
                        definition=self.definition,
                        parameters=parameters,
                        market_data=market_data,
                    )
                )

            output = response.data

            return output
        except Exception as err:
            check_exception_and_raise(err)

    def value(
        self,
        *,
        parameters: Optional[PricingParameters] = None,
        market_data: Optional[MarketDataInput] = None,
    ) -> FxForwardAnalyticsValuation:
        """
        Valuate a FX Forward Instrument (post-trade). Currently, only NextBusinessDay is supported for the date moving convention in the start date or end date.

        Parameters
        ----------
        parameters : PricingParameters, optional
            Base cross asset calculation parameters.
        market_data : MarketDataInput, optional
            An object defining market data to be used to compute the analytics.

        Returns
        --------
        FxForwardAnalyticsValuation
            Object defining the output of a FX Forward valuation analysis.

        Examples
        --------
        Calling value on a FxForward instance

        >>> fx_forward_client.value()
        {'description': {'endDate': {'adjusted': '2023-04-14', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': '', 'referenceDate': 'SpotDate', 'tenor': '6M', 'unAdjusted': '2023-04-14'}, 'startDate': {'adjusted': '2022-10-14', 'date': '2022-10-14', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': '', 'referenceDate': 'ValuationDate', 'unAdjusted': '2022-10-14'}, 'valuationDate': '2022-10-12'}, 'greeks': {'deltaAmountInContraCcy': 1984832.58230644, 'deltaAmountInDealCcy': 1985823.52830793, 'deltaAmountInReportCcy': None, 'deltaPercent': 99.241629115322}, 'valuation': {'MarketValueInContraCcy': -1946.96324985491, 'MarketValueInDealCcy': -2017.36040419212, 'MarketValueInReportCcy': None}}

        Calling value on a FxForward instance with parameters.

        >>> fx_forward_client.value(
        >>>     parameters=PricingParameters(
        >>>         valuation_date=datetime.date(2022, 10, 12),
        >>>     ),
        >>>     market_data=MarketDataInput(
        >>>         fx_forward_curves=[FxForwardCurveAsMarketDataInput(cross_currency=CrossCurrencyInput(code="USD"))]
        >>>     )
        >>> )
        {'description': {'endDate': {'adjusted': '2023-04-14', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': '', 'referenceDate': 'SpotDate', 'tenor': '6M', 'unAdjusted': '2023-04-14'}, 'startDate': {'adjusted': '2022-10-14', 'date': '2022-10-14', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': '', 'referenceDate': 'ValuationDate', 'unAdjusted': '2022-10-14'}, 'valuationDate': '2022-10-12'}, 'greeks': {'deltaAmountInContraCcy': 1984832.58230644, 'deltaAmountInDealCcy': 1985823.52830793, 'deltaAmountInReportCcy': None, 'deltaPercent': 99.241629115322}, 'valuation': {'MarketValueInContraCcy': -1946.96324985491, 'MarketValueInDealCcy': -2017.36040419212, 'MarketValueInReportCcy': None}}

        Calling value on a FxForward instance with parameters, using a definition of a pre-loaded curve.

        >>> eurgbp_curve = load(space='LSEG', name='EUR CAD FxForward')
        >>> eurgbp_fxfwd = FxForward(
        >>>     definition=(FxForwardInstrument(
        >>>     fx_rate=FxRate(cross_currency="EURCAD", rate=0.9),
        >>>     end_date=RelativeAdjustableDate(tenor="4M"),
        >>>     start_date=RelativeAdjustableDate(tenor="2M"),
        >>>     deal_amount=34000
        >>>     )
        >>>     ))
        >>> market_data = MarketDataInput()
        >>> market_data.fx_forward_curves.append(eurgbp_curve.definition)
        >>> eurgbp_fxfwd.value(market_data=market_data, parameters=PricingParameters(valuation_date="2024-06-10"))
        {'description': {'valuationDate': '2024-06-10', 'startDate': {'unAdjusted': '2024-08-12', 'adjusted': '2024-08-12', 'dateMovingConvention': 'NextBusinessDay', 'tenor': '2M'}, 'endDate': {'unAdjusted': '2024-10-12', 'adjusted': '2024-10-15', 'dateMovingConvention': 'NextBusinessDay', 'tenor': '4M'}}, 'valuation': {'discountFactor': 0.993299012538292, 'marketValueInDealCcy': 13224.0015210272, 'marketValueInContraCcy': 19586.1879032919}, 'greeks': {'deltaPercent': 99.3299012538292, 'deltaAmountInDealCcy': 20462.2750180567, 'deltaAmountInContraCcy': 33772.1664263019}}

        """

        try:

            response = None

            if self._id:

                response = check_and_raise(
                    Client().fx_forward_resource.value(
                        instrument_id=self._id,
                        parameters=parameters,
                        market_data=market_data,
                    )
                )
            else:

                response = check_and_raise(
                    Client().fx_forwards_resource.value(
                        definition=self.definition,
                        parameters=parameters,
                        market_data=market_data,
                    )
                )

            output = response.data

            return output
        except Exception as err:
            check_exception_and_raise(err)

    def save(self, *, name: Optional[str] = None, space: Optional[str] = None) -> bool:
        """
        Save FxForward instance in the platform store.

        Parameters
        ----------
        name : str, optional
            The FxForward name. The name parameter must be specified when the object is first created. Thereafter it is optional.
        space : str, optional
            The space where the FxForward is stored. Space is like a namespace where resources are stored. By default there are two spaces:
            LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

        Returns
        --------
        bool, optional
            True, if saved successfully, otherwise None


        Examples
        --------
        Save the instance with name and space.

        >>> fx_forward.save(name="MyCurve", space="MySpace")
        True

        """
        try:
            logger.info(f"Saving FxForward")
            if self._id:
                if name and name != self._location.name or (space and space != self._location.space):
                    raise LibraryException("When saving an existing resource, you may not change the name or space")
                self._overwrite()
                logger.info(f"FxForward saved")
            elif name:
                location = Location(name=name, space=space)
                self._create(location=location)
                logger.info(f"FxForward saved to space: {self._location.space} name: {self._location.name}")
            else:
                raise LibraryException("When saving for the first time, name must be defined.")
            return True
        except Exception as err:
            logger.info(f"FxForward save failed")
            check_exception_and_raise(err)

    def clone(self) -> "FxForward":
        """
        Return the same object, without id, name and space

        Parameters
        ----------


        Returns
        --------
        FxForward
            The cloned FxForward object


        Examples
        --------
        Clone the existing instance on definition and description.

        >>> fx_forward_clone = fx_forward.clone()

        """
        definition = self._definition_class()
        definition._data = copy.deepcopy(self.definition._data)
        description = None
        if self.description:
            description = Description()
            description._data = copy.deepcopy(self.description._data)
        return self.__class__(definition=definition, description=description)
