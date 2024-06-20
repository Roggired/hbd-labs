package hbd.service.domain.service

import hbd.service.domain.entity.DeliveryManEntity
import hbd.service.domain.entity.DeliveryEntity
import hbd.service.domain.repository.OrderRepository
import hbd.service.http.DeliverymanRequest
import hbd.service.http.OrderRequest
import hbd.service.http.PageView
import org.springframework.data.domain.Page
import org.springframework.data.domain.PageRequest
import org.springframework.data.domain.Sort
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate
import org.springframework.stereotype.Service
import java.time.LocalDateTime
import javax.sql.DataSource

@Service
class DeliveryService(
    private val orderRepository: OrderRepository,
    private val dataSource: DataSource,
) {

    fun getAllDeliveryMen(
        pageSize: Int,
        pageNumber: Int,
        request: DeliverymanRequest,
    ): PageView<DeliveryManEntity> {
        val template = NamedParameterJdbcTemplate(dataSource)
        return PageView(
            totalElements = 0,
            totalPages = 0,
            content = template.query(
                """
                SELECT * FROM delivery_man
                ORDER BY id
                OFFSET :offset
                LIMIT :limit
            """.trimIndent(),
                mapOf(
                    "offset" to request.numberOfDeliverymansToSkip + pageSize * pageNumber,
                    "limit" to pageSize,
                )
            ) { it, rowNum ->
                DeliveryManEntity(
                    id = it.getString(1),
                    name = it.getString(2),
                )
            }
        )
    }

    fun getAllOrders(
        pageSize: Int,
        pageNumber: Int,
        orderRequest: OrderRequest
    ): Page<DeliveryEntity> = orderRepository.findAllFiltered(
        deliveryTimeFilterClause = LocalDateTime.parse(orderRequest.deliveryTimeFilterClause),
        pageable = PageRequest.of(pageNumber, pageSize, Sort.by("orderDateCreated"))
    )
}
