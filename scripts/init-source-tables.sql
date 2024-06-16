CREATE TABLE dish
(
	dish_id BIGSERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	price BIGINT NOT NULL
);

CREATE TABLE category
(
	category_id BIGSERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	percent INT NOT NULL,
	min_payment INT NOT NULL
);

CREATE TABLE client
(
	client_id BIGSERIAL PRIMARY KEY,
	bonus_balance BIGINT NOT NULL,
	category_id BIGINT REFERENCES category(category_id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE payment
(
	payment_id BIGSERIAL PRIMARY KEY,
	client_id BIGINT REFERENCES client(client_id) ON DELETE CASCADE NOT NULL,
	dish_id BIGINT REFERENCES dish(dish_id) ON DELETE CASCADE NOT NULL,
	dish_amount INT NOT NULL,
	order_id VARCHAR(255) NOT NULL,
	order_time TIMESTAMP NOT NULL,
	order_sum BIGINT NOT NULL,
	tips BIGINT NOT NULL
);

CREATE TYPE log_action AS ENUM ('INSERT', 'UPDATE', 'DELETE');

CREATE TABLE logs
(
	id BIGSERIAL PRIMARY KEY,
    entity_id BIGINT NOT NULL,
	table_name VARCHAR(255) NOT NULL,
	"time" TIMESTAMP NOT NULL,
	"values" JSONB,
	action log_action
);

CREATE FUNCTION log_trigger() RETURNS TRIGGER AS
$$
DECLARE
    entity_id BIGINT;
	new_values JSONB;
	updated_values JSONB;
	removed_values JSONB;
BEGIN
	IF (TG_OP = 'INSERT') THEN
		new_values := row_to_json(NEW);

		IF (TG_TABLE_NAME = 'dish') THEN
            entity_id := NEW.dish_id;
        ELSIF (TG_TABLE_NAME = 'category') THEN
		    entity_id := NEW.category_id;
		ELSIF (TG_TABLE_NAME = 'client') THEN
		    entity_id := NEW.client_id;
		ELSIF (TG_TABLE_NAME = 'payment') THEN
		    entity_id := NEW.payment_id;
        END IF;

		INSERT INTO logs(entity_id, table_name, "time", "values", action) VALUES(entity_id, TG_TABLE_NAME, now(), new_values, 'INSERT');
		RETURN NEW;
	ELSIF (TG_OP = 'UPDATE') THEN
		updated_values := row_to_json(NEW);

		IF (TG_TABLE_NAME = 'dish') THEN
            entity_id := NEW.dish_id;
        ELSIF (TG_TABLE_NAME = 'category') THEN
		    entity_id := NEW.category_id;
		ELSIF (TG_TABLE_NAME = 'client') THEN
		    entity_id := NEW.client_id;
		ELSIF (TG_TABLE_NAME = 'payment') THEN
		    entity_id := NEW.payment_id;
        END IF;

		INSERT INTO logs(entity_id, table_name, "time", "values", action) VALUES(entity_id, TG_TABLE_NAME, now(), updated_values, 'UPDATE');
		RETURN NEW;
	ELSIF (TG_OP = 'DELETE') THEN
		removed_values := row_to_json(OLD);

		IF (TG_TABLE_NAME = 'dish') THEN
            entity_id := OLD.dish_id;
        ELSIF (TG_TABLE_NAME = 'category') THEN
		    entity_id := OLD.category_id;
		ELSIF (TG_TABLE_NAME = 'client') THEN
		    entity_id := OLD.client_id;
		ELSIF (TG_TABLE_NAME = 'payment') THEN
		    entity_id := OLD.payment_id;
        END IF;

		INSERT INTO logs(entity_id, table_name, "time", "values", action) VALUES(entity_id, TG_TABLE_NAME, now(), removed_values, 'DELETE');
		RETURN OLD;
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_dish
AFTER UPDATE OR INSERT OR DELETE ON dish FOR EACH ROW
EXECUTE FUNCTION log_trigger();

CREATE TRIGGER check_category
AFTER UPDATE OR INSERT OR DELETE ON category FOR EACH ROW
EXECUTE FUNCTION log_trigger();

CREATE TRIGGER check_client
AFTER UPDATE OR INSERT OR DELETE ON client FOR EACH ROW
EXECUTE FUNCTION log_trigger();

CREATE TRIGGER check_payment
AFTER UPDATE OR INSERT OR DELETE ON payment FOR EACH ROW
EXECUTE FUNCTION log_trigger();
