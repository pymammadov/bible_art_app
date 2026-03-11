import { Component } from 'react';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error) {
    console.error('Unhandled frontend error:', error);
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="mx-auto mt-10 max-w-3xl rounded-lg border border-red-200 bg-red-50 p-6 text-red-700">
          <h1 className="text-lg font-semibold">Something went wrong</h1>
          <p className="mt-2 text-sm">The page crashed unexpectedly. Please reload and try again.</p>
          <button
            type="button"
            onClick={this.handleReload}
            className="mt-4 rounded-md bg-red-600 px-3 py-2 text-sm font-medium text-white hover:bg-red-700"
          >
            Reload app
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
