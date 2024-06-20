package hbd.service.http

import hbd.service.domain.entity.DeliveryManEntity
import hbd.service.domain.entity.DeliveryEntity
import hbd.service.domain.service.DeliveryService
import org.springframework.data.domain.Page
import org.springframework.validation.annotation.Validated
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/v1/delivery/")
class DeliveryController(
    private val deliveryService: DeliveryService
) {

    @PostMapping("/orders")
    fun getAllOrders(
        @RequestParam pageSize: Int,
        @RequestParam pageNumber: Int,
        @RequestBody @Validated orderRequest: OrderRequest
    ): PageView<DeliveryEntity> = deliveryService.getAllOrders(
        pageSize = pageSize,
        pageNumber = pageNumber,
        orderRequest = orderRequest,
    ).toView()


    @PostMapping("/delivers")
    fun getAllDeliveryMen(
        @RequestParam pageSize: Int,
        @RequestParam pageNumber: Int,
        @RequestBody @Validated request: DeliverymanRequest,
    ): PageView<DeliveryManEntity> = deliveryService.getAllDeliveryMen(
        pageSize = pageSize,
        pageNumber = pageNumber,
        request = request,
    )
}

data class PageView<T>(
    val totalElements: Long,
    val totalPages: Int,
    val content: List<T>
)

fun <T> Page<T>.toView(): PageView<T> = PageView(
    totalElements = totalElements,
    totalPages = totalPages,
    content = content,
)

data class OrderRequest(
    val deliveryTimeFilterClause: String,
)

data class DeliverymanRequest(
    val numberOfDeliverymansToSkip: Int,
)
