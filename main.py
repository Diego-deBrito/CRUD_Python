"""
Aplicação Desktop em Python com PyQt5.
Funcionalidades:
- Cadastro de pessoas (nome e email)
- Listagem em tabela
- Edição de registros
- Exclusão de registros

Este projeto demonstra:
- Conhecimento em GUI com PyQt5
- Integração com banco de dados SQLite
- Implementação de CRUD completo
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox
)
import database


class CRUDApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Pessoas")
        self.setGeometry(200, 200, 600, 400)

        # Layout principal
        self.layout = QVBoxLayout()

        # Campos de entrada
        self.nome_input = QLineEdit(self)
        self.nome_input.setPlaceholderText("Nome")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")

        # Botões de ação
        self.btn_add = QPushButton("Adicionar", self)
        self.btn_update = QPushButton("Atualizar", self)
        self.btn_delete = QPushButton("Excluir", self)

        # Conexão dos botões com funções
        self.btn_add.clicked.connect(self.adicionar)
        self.btn_update.clicked.connect(self.atualizar)
        self.btn_delete.clicked.connect(self.excluir)

        # Layout para os campos de entrada e botões
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.nome_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.btn_add)
        form_layout.addWidget(self.btn_update)
        form_layout.addWidget(self.btn_delete)

        # Tabela de registros
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Email"])
        self.table.cellClicked.connect(self.preencher_campos)

        # Montagem do layout
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        # Carregar dados do banco
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega todos os registros do banco e exibe na tabela."""
        self.table.setRowCount(0)
        dados = database.listar()
        for row_num, row_data in enumerate(dados):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def adicionar(self):
        """Adiciona um novo registro no banco."""
        nome = self.nome_input.text()
        email = self.email_input.text()
        if nome and email:
            try:
                database.inserir(nome, email)
                self.carregar_dados()
                self.nome_input.clear()
                self.email_input.clear()
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível adicionar: {e}")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")

    def atualizar(self):
        """Atualiza o registro selecionado."""
        selected = self.table.currentRow()
        if selected >= 0:
            id_ = int(self.table.item(selected, 0).text())
            nome = self.nome_input.text()
            email = self.email_input.text()
            try:
                database.atualizar(id_, nome, email)
                self.carregar_dados()
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Não foi possível atualizar: {e}")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um registro para atualizar.")

    def excluir(self):
        """Exclui o registro selecionado."""
        selected = self.table.currentRow()
        if selected >= 0:
            id_ = int(self.table.item(selected, 0).text())
            resposta = QMessageBox.question(
                self, "Confirmação",
                "Deseja realmente excluir este registro?",
                QMessageBox.Yes | QMessageBox.No
            )
            if resposta == QMessageBox.Yes:
                try:
                    database.deletar(id_)
                    self.carregar_dados()
                except Exception as e:
                    QMessageBox.warning(self, "Erro", f"Não foi possível excluir: {e}")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um registro para excluir.")

    def preencher_campos(self, row, column):
        """Preenche os campos de entrada com os dados da linha selecionada."""
        self.nome_input.setText(self.table.item(row, 1).text())
        self.email_input.setText(self.table.item(row, 2).text())


if __name__ == "__main__":
    database.init_db()
    app = QApplication(sys.argv)
    window = CRUDApp()
    window.show()
    sys.exit(app.exec_())
