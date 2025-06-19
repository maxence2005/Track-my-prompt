// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick

Window {
    minimumWidth: 1100
    minimumHeight: 600

    visibility: "Maximized"
    visible: true
    title: "TrackMyPrompts"

    property bool isLoaded: false

    Loader {
        anchors.fill: parent
        id: pageLoader
        sourceComponent: isLoaded ? appViewComponent : loadingScreenComponent
    }

    Component {
        id: appViewComponent
        AppView {}
    }

    Component {
        id: loadingScreenComponent
        LoadingScreen {}
    }
}

