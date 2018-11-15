
import React, { Component } from 'react'
import { Menu, Icon } from 'antd'
import { connect } from 'dva'

import { Link, routerRedux } from 'dva/router'

class Header extends Component {
    render() {
        const { location } = this.props
        return (
            <Menu
                // selectedKeys={[location.pathname]}
                mode="horizontal"
                theme="dark"
            >

                {/* <Menu.Item key="/">
                    <Link to="/">
                        <Icon type="home" />Home
                    </Link>
                </Menu.Item> */}

                <Menu.Item key="/top5 ">
                    <Link to="/top5">
                        <Icon type="bars" />Top 5
                    </Link>
                </Menu.Item>
                <Menu.Item key="/signals">
                    <Link to="/signals">
                        <Icon type="bars" />signal
                    </Link>
                </Menu.Item>

                {/* <Menu.Item key="/zfline">
                    <Link to="/zfline">
                        <Icon type="bars" />zfline
                    </Link>
                </Menu.Item> */}

                <Menu.Item key="/test">
                    <Link to="/test">
                        <Icon type="bars" />test
                    </Link>
                </Menu.Item>


                {/* <Menu.Item key="/404">
                    <Link to="/page-you-dont-know">
                        <Icon type="frown-circle" />404
                    </Link>
                </Menu.Item>
                <Menu.Item key="/antd">
                    <a href="https://www.baidu.com">w000m</a>
                </Menu.Item> */}
            </Menu>
        )
    }
}

export default connect()(Header)


