package hbd.service.http.request

import org.springframework.data.domain.Sort.Direction
import java.time.LocalDateTime

data class OrderRequest(
    val sortField: List<OrderSort>?
)

data class OrderDto(
    val deliveryId: String,
    val deliveryManId: String,
    val deliveryAddress: String,
    val deliveryTime: LocalDateTime,
    val rating: Double,
    val tips: Double?
)


data class OrderSort(
    val field: OrderField,
    val order: Direction
)

enum class OrderField(
    val fieldName: String
) {
    ID("id"),
    ORDER_DATE_CREATE("order_date_created"),
    DELIVERY_ID("delivery_id"),
    DELIVERYMAN_ID("deliveryman_id"),
    DELIVERY_ADDRESS("delivery_address"),
    DELIVERY_TIME("delivery_time"),
    RATING("rating"),
    TIPS("tips")
}
