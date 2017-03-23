 (function(window) {
     function CBNTabs(el) {
         this.el = el;
         this._init()
     };

     CBNTabs.prototype._init = function() {
         this.tabs = [].slice.call(this.el.querySelectorAll('nav > ul > li'));
         this.items = [].slice.call(this.el.querySelectorAll('.content-wrap > section'));
         this.current = -1;
         this._show();
         this._initEvent()
     }

     CBNTabs.prototype._initEvent = function() {
         var self = this;
         this.tabs.forEach(function(tab, index) {
             tab.addEventListener('click', function(e) {
                 e.preventDefault();
                 self._show(index)
             })
         })
     }

     CBNTabs.prototype._show = function(index) {
         if (this.current >= 0) {
             this.tabs[this.current].className = this.items[this.current].className = '';
         }
         this.current = index != undefined ? index : 0;
         this.tabs[this.current].className = 'tab-current';
         this.items[this.current].className = 'content-current';
     }

     window.CBNTabs = CBNTabs;
 })(window);
