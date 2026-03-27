START TRANSACTION;

-- Selecciona la base de datos creada por Docker
USE api_django;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name ENUM('admin','user') UNIQUE NOT NULL,
    description VARCHAR(60)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    token VARCHAR(500),
    ip_address VARCHAR(50),
    user_agent VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE auth_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(50),
    ip_address VARCHAR(50),
    user_agent VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

-- para RBAC (tabla de permisos)

CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255)
);

-- Tabla intermedia para relación roles-permisos
CREATE TABLE role_permissions (
    role_id INT,
    permission_id INT,
    PRIMARY KEY(role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);


-- ===============================
-- INSERTS INICIALES
-- ===============================
-- Roles

INSERT INTO roles (name, description) VALUES
('admin', 'Administrador del sistema'),
('user', 'Usuario normal');

-- Ejemplo de permisos
INSERT INTO permissions (name, description) VALUES
('read_users', 'Leer usuarios'),
('create_users', 'Crear usuarios'),
('delete_users', 'Eliminar usuarios'),
('view_logs', 'Ver logs');

-- Asignar permisos a rol admin
INSERT INTO role_permissions VALUES (1,1);
INSERT INTO role_permissions VALUES (1,2);
INSERT INTO role_permissions VALUES (1,3);
INSERT INTO role_permissions VALUES (1,4);

-- Usuario admin inicial (la password luego se reemplaza por hash)
INSERT INTO users (username, email, password_hash, role_id)
VALUES ('admin', 'admin@email.com', 'password_temporal', 1); 
-- ojo parsear la función hash la contraseña de administrador.

COMMIT;