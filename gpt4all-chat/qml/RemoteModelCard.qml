import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Dialogs
import Qt.labs.folderlistmodel
import Qt5Compat.GraphicalEffects

import llm
import chatlistmodel
import download
import modellist
import network
import gpt4all
import mysettings
import localdocs


Rectangle {
    property alias providerName: providerNameLabel.text
    property alias providerImage: myimage.source
    property alias providerDesc: providerDescLabel.helpText
    property string providerBaseUrl: ""
    property bool providerIsCustom: false
    property var filterModels: function(names) {
        return names;
    };

    color: theme.conversationBackground
    radius: 10
    border.width: 1
    border.color: theme.controlBorder
    implicitHeight: topColumn.height + bottomColumn.height + 60

    ColumnLayout {
        id: topColumn
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 20
        spacing: 30
        RowLayout {
            Layout.alignment: Qt.AlignTop
            spacing: 10
            Rectangle {
                id: rec
                color: "transparent"
                Layout.preferredWidth: 48
                Layout.preferredHeight: 48
                Layout.alignment: Qt.AlignLeft
                Image {
                    id: myimage
                    anchors.centerIn: parent
                    sourceSize.width: rec.width
                    sourceSize.height: rec.height
                    mipmap: true
                    visible: false
                    fillMode: Image.PreserveAspectFit

                }

                ColorOverlay {
                    anchors.fill: myimage
                    source: myimage
                }
            }

            Label {
                id: providerNameLabel
                color: theme.textColor
                font.pixelSize: theme.fontSizeBanner
            }
        }

        MySettingsLabel {
            id: providerDescLabel
            onLinkActivated: function(link) { Qt.openUrlExternally(link) }
        }
    }

    ColumnLayout {
        id: bottomColumn
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 20
        spacing: 30

        ColumnLayout {
            MySettingsLabel {
                text: qsTr("API Key")
                font.bold: true
                font.pixelSize: theme.fontSizeLarge
                color: theme.settingsTitleTextColor
            }

            MyTextField {
                id: apiKeyField
                Layout.fillWidth: true
                wrapMode: Text.WrapAnywhere
                function showError() {
                    messageToast.show(qsTr("ERROR: $API_KEY is empty."));
                    apiKeyField.placeholderTextColor = theme.textErrorColor;
                }
                onTextChanged: {
                    apiKeyField.placeholderTextColor = theme.mutedTextColor;
                    if (!providerIsCustom) {
                        myModelList.model = filterModels(ModelList.remoteModelList(apiKeyField.text, providerBaseUrl));
                        myModelList.currentIndex = -1;
                    }
                }
                placeholderText: qsTr("enter $API_KEY")
                Accessible.role: Accessible.EditableText
                Accessible.name: placeholderText
                Accessible.description: qsTr("Whether the file hash is being calculated")
            }
        }

        ColumnLayout {
            visible: providerIsCustom
            MySettingsLabel {
                text: qsTr("Base Url")
                font.bold: true
                font.pixelSize: theme.fontSizeLarge
                color: theme.settingsTitleTextColor
            }
            MyTextField {
                id: baseUrlField
                Layout.fillWidth: true
                wrapMode: Text.WrapAnywhere
                function showError() {
                    messageToast.show(qsTr("ERROR: $BASE_URL is empty."));
                    baseUrlField.placeholderTextColor = theme.textErrorColor;
                }
                onTextChanged: {
                    baseUrlField.placeholderTextColor = theme.mutedTextColor;
                }
                placeholderText: qsTr("enter $BASE_URL")
                Accessible.role: Accessible.EditableText
                Accessible.name: placeholderText
            }
        }
        ColumnLayout {
            visible: providerIsCustom
            MySettingsLabel {
                text: qsTr("Model Name")
                font.bold: true
                font.pixelSize: theme.fontSizeLarge
                color: theme.settingsTitleTextColor
            }
            MyTextField {
                id: modelNameField
                Layout.fillWidth: true
                wrapMode: Text.WrapAnywhere
                function showError() {
                    messageToast.show(qsTr("ERROR: $MODEL_NAME is empty."))
                    modelNameField.placeholderTextColor = theme.textErrorColor;
                }
                onTextChanged: {
                    modelNameField.placeholderTextColor = theme.mutedTextColor;
                }
                placeholderText: qsTr("enter $MODEL_NAME")
                Accessible.role: Accessible.EditableText
                Accessible.name: placeholderText
            }
        }

        ColumnLayout {
            visible: myModelList.count > 0 && !providerIsCustom

            MySettingsLabel {
                text: qsTr("Models")
                font.bold: true
                font.pixelSize: theme.fontSizeLarge
                color: theme.settingsTitleTextColor
            }

            RowLayout {
                spacing: 10

                MyComboBox {
                    Layout.fillWidth: true
                    id: myModelList
                    currentIndex: -1;
                }
            }
        }

        MySettingsButton {
            id: installButton
            Layout.alignment: Qt.AlignRight
            text: qsTr("Install")
            font.pixelSize: theme.fontSizeLarge

            property string apiKeyText: apiKeyField.text.trim()
            property string baseUrlText: providerIsCustom ? baseUrlField.text.trim() : providerBaseUrl.trim()
            property string modelNameText: providerIsCustom ? modelNameField.text.trim() : myModelList.currentText.trim()

            enabled: apiKeyText !== "" && baseUrlText !== "" && modelNameText !== ""

            onClicked: {
                Download.installCompatibleModel(
                            modelNameText,
                            apiKeyText,
                            baseUrlText,
                            );
                myModelList.currentIndex = -1;
            }
            Accessible.role: Accessible.Button
            Accessible.name: qsTr("Install")
            Accessible.description: qsTr("Install remote model")
        }
    }
}
