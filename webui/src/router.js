import React from 'react';
import { Router, Route, Switch, routerRedux  } from 'dva/router';

// import IndexPage from './routes/IndexPage';
// import MainForm from './routes/MainForm';
// import User from './routes/user';
import App from './routes/App'
import dynamic from 'dva/dynamic' // 路由按需加载


const { ConnectedRouter } = routerRedux



function RouterConfig({ history, app  }) {

  // const IndexPage = dynamic({
  //   app,
  //   component: () => import('./routes/IndexPage')
  // })  

  const Top5 = dynamic({
    app,
    component: () => import('./routes/Top5')
  })

  const Signalzf = dynamic({
    app,
    component: () => import('./routes/Signalzf')
  })
  const ZFline = dynamic({
    app,
    component: () => import('./routes/ZFline')
  })
  const Fst = dynamic({
    app,
    component: () => import('./routes/Fst')
  })  
  const Test = dynamic({
    app,
    component: () => import('./routes/Test')
  })  

  return (
    <ConnectedRouter history={history }>
    <App>
      <Switch>

        <Route path="/" exact component={ Top5 } /> 
        {/* <Route path="/" exact component={ MainForm } />  */}
        <Route path="/Top5" exact component={Top5} />
        <Route path="/signals" exact component={Signalzf} />
        <Route path="/fst" exact component={Fst} />
        <Route path="/zfline/:code" exact component={ZFline} />
        <Route path="/test" exact component={Test} />
        
      </Switch>
      </App>  
    </ConnectedRouter>
  );
}

export default RouterConfig;
